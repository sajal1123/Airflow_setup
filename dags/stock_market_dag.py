from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests

# Define default_args dictionary to configure your DAG
default_args = {
    'owner': 'finance',
    'start_date': datetime(2023, 12, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

extracted_data = {}

# Instantiate a DAG using the with statement
with DAG(
    dag_id = 'stock_market_etl',
    default_args=default_args,
    description='ETL process for stock market data',
    schedule_interval="0 12 * * *",  # Set your desired schedule
) as dag:

    def extract_data(**kwargs):
        global extracted_data
        # Alpha Vantage API key (replace 'YOUR_API_KEY' with your actual key)
        api_key = 'VME4WFAH35TA8DIZ'

        # Define the stocks you're interested in
        stocks = ['GOOGL', 'AAPL', 'NFLX', 'FB', 'MSFT', 'AMZN']

        # Loop through each stock and make API requests
        for stock_symbol in stocks:
            # Alpha Vantage API endpoint for time series data
            api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval=5min&apikey={api_key}'

            # Make the API request
            response = requests.get(api_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                stock_data = response.json()

                # Extract the relevant information (adjust this based on Alpha Vantage response structure)
                time_series_data = stock_data.get('Time Series (5min)', {})
                latest_data = list(time_series_data.values())

                # Store the extracted data
                extracted_data[stock_symbol] = latest_data
            else:
                print(f"Failed to fetch data for {stock_symbol}. Status code: {response.status_code}")

        # You can do more with the extracted data, such as logging or saving it to XCom for downstream tasks
        print("Extracted stock market data:", extracted_data)

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_data,
        provide_context=True,
    )

    def transform_data(**kwargs):
        # Placeholder for data transformation logic
        print("Transforming stock market data")

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_data,
        provide_context=True,
    )

    def load_data(**kwargs):
        # Placeholder for data loading logic
        print("Loading stock market data to PostgreSQL")

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load_data,
        provide_context=True,
    )

    # Set up task dependencies
    extract_task >> transform_task >> load_task
