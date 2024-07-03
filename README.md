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
   ```
    CREATE DATABASE WeatherDB;
    GO

    USE WeatherDB;
    GO

    CREATE TABLE WeatherData (
        id INT PRIMARY KEY IDENTITY(1,1),
        datetime DATETIME DEFAULT GETDATE(),
        name NVARCHAR(100),
        temperature FLOAT,
        pressure FLOAT,
        humidity FLOAT,
        wind NVARCHAR(100)
       );
     GO
   ```
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


## Dependencies 

- Requests
- Pyodbc
- Pandas 2.2.2


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




## Acknowledgments
- **openweathermap** for providing the weather data. 
- **pyodbc** for database connectivity.
- **pandas** for data manipulation and analysis (version 2.2.2)
- **requests** for handling http requests. 


