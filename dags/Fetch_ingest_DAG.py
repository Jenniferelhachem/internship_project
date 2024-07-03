from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from fetching import fetch
from ingestion import ingest
from datetime import datetime, timedelta
import requests
import json
import pandas as pd
import pyodbc
import os

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 25),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'weather_data_pipeline',
    default_args=default_args,
    description='A DAG to fetch weather data and ingest into SQL Server',
    schedule_interval='@hourly',  
)

# Define tasks in the DAG
fetch_weather_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch,
    dag=dag,
)

ingest_to_sql_task = PythonOperator(
    task_id='ingest_to_sql_server',
    python_callable=ingest,
    dag=dag,
)

# Set task dependencies
fetch_weather_task >> ingest_to_sql_task
