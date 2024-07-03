from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
import requests
import json
import pandas as pd

def fetch_data():
    # we define the function that fetches the data 
    # Define the API URL
    url = "https://api.openweathermap.org/data/2.5/weather?appid=a2b2e442aba806b89cc7e799526a1158&lon=35.5018&lat=33.8938"

    # Make the API call
    response = requests.get(url)
    temp_json = response.text

    # Load data, changing JSON string to Python dictionary
    data = json.loads(temp_json)

    # Normalize the data into a table
    df = pd.json_normalize(data)

    # Convert 'dt' to a datetime object
    df['dt'] = pd.to_datetime(df['dt'], unit='s')
    
    # Extract details from the nested list in the 'weather' column into separate columns
    weather_data = df['weather'].apply(pd.Series)[0]
    df['weather_main'] = weather_data.apply(lambda x: x['main'])
    df['weather_description'] = weather_data.apply(lambda x: x['description'])
    df['weather_icon'] = weather_data.apply(lambda x: x['icon'])

    # Drop the original 'weather' column
    df = df.drop(columns=['weather'])

    # Rename columns
    df = df.rename(columns=lambda x: x.replace('main.', '') if 'main.' in x else x)
    df = df.rename(columns={"dt": "datetime", "temp": "temperature","wind.speed":"wind"})
    df = df[["datetime","name","temperature","pressure","humidity","wind"]]
    df["temperature"] = round(df["temperature"] - 273.15,2)
    
    # Save the DataFrame to a CSV file
    df.to_csv("fetching/api_output.csv", index=False)
    print("CSV file created successfully.")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('Fetch_Data', 
         default_args=default_args,
         description='A simple DAG to fetch and process data',
         schedule=timedelta(days=1),  #Run daily
         catchup=False) as dag:

    start_task = EmptyOperator(task_id='start_task', 
                               dag=dag)

    fetch_task = PythonOperator(task_id='fetch_data',
                                python_callable=fetch_data,
                                dag=dag)

    end_task = EmptyOperator(task_id='end_task',
                             dag=dag)

    start_task >> fetch_task >> end_task

