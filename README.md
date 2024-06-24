# Weather Data Ingestion Project

## Overview

This project involves fetching weather data from a Weather API and ingesting it into an MSSQL Server database. The purpose is to collect and store weather data for further analysis and reporting.

## Features

- Fetch the current weather data from the specified Weather API.
- Transform and clean the data as needed.
- Insert the data into an MSSQL Server database.
- Scheduled or on-demand data fetching using airflow.

## Prerequisites

- Python 3.10.12
- MSSQL Server
- Weather API Key

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/weather-data-ingestion.git
    cd weather-data-ingestion
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```
4. **Set up the MSSQL Server database:**

    Create a database and table to store the weather data. You can use the following SQL script as an example:

    ```sql
    CREATE DATABASE WeatherDB;
    GO

    USE WeatherDB;
    GO

    CREATE TABLE WeatherData (
        id INT PRIMARY KEY IDENTITY(1,1),
        location NVARCHAR(100),
        temperature FLOAT,
        humidity FLOAT,
        pressure FLOAT,
        weather_description NVARCHAR(255),
        fetch_time DATETIME DEFAULT GETDATE()
    );
    GO
    ```

## Configuration

1. **Set up the configuration file:**

    Create a `config.ini` file in the root directory of the project with the following content:

    ```ini
    [weather_api]
    api_key = YOUR_API_KEY
    base_url = https://api.weatherapi.com/v1/current.json

    [database]
    server = YOUR_SERVER_NAME
    database = WeatherDB
    username = YOUR_DB_USERNAME
    password = YOUR_DB_PASSWORD
    ```

2. **Replace the placeholders with your actual API key and database credentials.**

## Usage

1. **Run the data fetching script:**

    ```sh
    python fetch.py
    ```

    This script will fetch the weather data from the API.
2. **Run the data ingesting script:**
    ```sh
    python ingest.py
    ```
    This script will ingest the fetched data from the API and insert it into the MSSQL server database.


## Project Structure

1. Fetch.py
2. Ingest.py
3. Requirements.txt
4. README.md
5. Venv/


## Dependencies 
```
- Requests
- Pyodbc
- Pandas== 2.2.2

```
## Contributing

1. Clone the repository.
    ```plaintext
    git clone https://github.com/yourusername/weather-data-ingestion.git
    cd weather-data-ingestion
    ```

2. Create a new branch (`git checkout -b feature/your-feature-name`).
   
3. Make your changes.

4. Commit your changes (`git commit -m 'Add some feature'`).

5. Push to the branch (`git push origin feature/your-feature-name`).

6. Open a pull request.

## License 
This project is licensed under the MIT License.



## Acknowledgments
- **openweathermap** for providing the weather data. 
- **pyodbc** for database connectivity.
- **pandas** for data manipulation and analysis (version 2.2.2)
- **requests** for handling http requests. 


