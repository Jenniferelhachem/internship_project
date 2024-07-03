import requests
import json
import pandas as pd
from pathlib import Path

def fetch():
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
    # Display the DataFrame
    print(df)

    # Save the DataFrame to a CSV file
    output_file_path = Path("tmp/fetching/api_output.csv")
    output_file_path.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(output_file_path, index=False)
    print("CSV file created successfully.")