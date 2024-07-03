from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
import pandas as pd
import pyodbc
import os

def ingest_data():
    """
    Function to ingest data from a CSV file into a SQL Server database.
    """
    # Print the current working directory to help debug the path issue
    print("Current working directory:", os.getcwd())

    # Specify the path to your CSV file
    csv_file_path = 'fetching/api_output.csv'  # Update with the correct path

    # Read the CSV file
    try:
        df = pd.read_csv(csv_file_path)
        print(df.head())  # Print first few rows to verify
    except FileNotFoundError as e:
        print(f"Error: {e}. Please check if the file '{csv_file_path}' exists.")
        return

    # Remove duplicates based on datetime
    df.drop_duplicates(subset=['datetime'], inplace=True)

    # SQL Server connection string
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=DESKTOP-1R67MDQ;"         
        "DATABASE=testing;"     
        "UID=sa;"               
        "PWD=12345;"   
        "TrustServerCertificate=yes;"             
    )

    conn = None  # Initialize conn to None

    try:
        # Establish connection
        conn = pyodbc.connect(conn_str)
        
        # Check if connection is successful
        if conn:
            print("Connected to SQL Server successfully")
        else:
            print("Failed to connect to SQL Server")
            return

        cursor = conn.cursor()

        # Check if table WeatherData exists
        table_exists = cursor.tables(table='WeatherData').fetchone()
        if not table_exists:
            # Table does not exist, create it dynamically
            create_table_sql = """
            CREATE TABLE WeatherData (
                datetime DATETIME,
                name NVARCHAR(50),
                temperature FLOAT,
                pressure INT,
                humidity INT,
                wind FLOAT
            )
            """
            cursor.execute(create_table_sql)
            conn.commit()
            print("Table 'WeatherData' created")

        # Insert data into the table
        insert_sql = """
        INSERT INTO WeatherData (datetime, name, temperature, pressure, humidity, wind)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        # Iterate over cleaned DataFrame
        for index, row in df.iterrows():
            cursor.execute(insert_sql, row['datetime'], row['name'], row['temperature'], row['pressure'], row['humidity'], row['wind'])

        conn.commit()
        print("Data inserted successfully")

        # Remove duplicates in SQL Server table
        remove_duplicates_sql = """
        WITH CTE AS (
            SELECT 
                [datetime],
                [name],
                [temperature],
                [pressure],
                [humidity],
                [wind],
                ROW_NUMBER() OVER (PARTITION BY [datetime] ORDER BY (SELECT 0)) AS rn
            FROM [testing].[dbo].[WeatherData]
        )
        DELETE FROM CTE
        WHERE rn > 1;
        """
        cursor.execute(remove_duplicates_sql)
        conn.commit()
        print("Duplicates removed successfully")

    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server or executing SQL query: {e}")

    finally:
        # Close cursor and connection if they are defined
        if conn:
            cursor.close()
            conn.close()
            print("Connection to SQL Server closed")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('Ingest_Data', 
         default_args=default_args,
         description='A DAG to Ingest and process data with dependency on fetch',
         schedule_interval=timedelta(days=1),  # Run daily
         catchup=False) as dag:

    start_task = EmptyOperator(task_id='start_task', 
                               dag=dag)

    # Wait for the fetch DAG to complete
    wait_for_fetch_task = ExternalTaskSensor( #external task sensor waits for an execution to finish.
        task_id='wait_for_fetch_task',
        external_dag_id='fetch',  
        external_task_id='end_task', 
        mode='poke',  
        poke_interval=60,
        timeout=3600, 
        dag=dag,
    )

    ingest_task = PythonOperator(task_id='ingest_data',
                                 python_callable=ingest_data,
                                 dag=dag)

    end_task = EmptyOperator(task_id='end_task',
                             dag=dag)


    start_task >> wait_for_fetch_task >> ingest_task >> end_task
