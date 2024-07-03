import pyodbc


def aggregate():

    # SQL Server connection string
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=DESKTOP-1R67MDQ;"
        "DATABASE=testing;"
        "UID=sa;"
        "PWD=12345;"
        "TrustServerCertificate=yes;"
    )
    conn = None
    try:
        conn = pyodbc.connect(conn_str)
        if conn:
            print("Connected to SQL Server successfully")
        else:
            print("Failed to connect to SQL Server")
            exit(1)
        cursor = conn.cursor()
        # Check if table DailyWeatherData exists
        table_exists = cursor.tables(table="DailyWeatherData").fetchone()
        if not table_exists:
            # Table does not exist, create it dynamically
            create_table_sql = """
                CREATE TABLE DailyWeatherData (
                date DATE,
                Min_temperature FLOAT,
                Avg_temperature FLOAT,
                Min_humidity FLOAT,
                Avg_humidity FLOAT,
                Min_pressure FLOAT,
                Avg_pressure FLOAT
            );
            """
            cursor.execute(create_table_sql)
            print("Table 'DailyWeatherData' created")
        else:
            truncate_table = """
                truncate TABLE DailyWeatherData;
            """
            cursor.execute(truncate_table)
            print("Table 'DailyWeatherData' truncated")

        Average_sql = """
            insert into dbo.DailyWeatherData
            SELECT  cast(datetime as date) as date
                ,avg([temperature]) as Avg_temperature
                ,min(temperature) as Min_temperature
                ,avg([humidity]) as Avg_humidity
                ,min ([humidity]) as Min_humidity
                ,min ([pressure]) as Min_pressure
                ,avg ([pressure]) as Avg_pressure
            FROM [testing].[dbo].[WeatherData]
            group by cast(datetime as date) """
        cursor.execute(Average_sql)
        conn.commit()

    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server or executing SQL query: {e}")
    except Exception as e:
        print(e)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Connection to SQL Server closed")
