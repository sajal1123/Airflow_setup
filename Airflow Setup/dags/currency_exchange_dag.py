from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
import requests

default_args = {
    'owner': 'currency',
    'start_date': datetime(2023, 12, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

def clean_currency(currency):
    cleaned_currency = ''.join(char.lower() for char in currency if char.isalpha())
    return cleaned_currency

def get_currency_exchange(base_currency, currency_list, date):
    base_currency = clean_currency(base_currency)
    exchange_rates = {"date": date, "base_currency": base_currency}

    for currency in currency_list:
        currency = clean_currency(currency)
        api = f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/{date}/currencies/{base_currency}/{currency}.json'
        response = requests.get(api)

        if response.status_code == 200:
            exchange_value = response.json()[currency]
            exchange_rates[currency] = exchange_value
        else:
            print(f'Failed to fetch exchange rate for {currency}')
    return exchange_rates

def fetch_exchange_rates_task(**kwargs):
    ti = kwargs['ti']
    base_currency = 'usd'
    curr_list = ["eur", "jpy", "inr"]
    date = ti.execution_date.strftime('%Y-%m-%d')
    exchange_rates_data = get_currency_exchange(base_currency, curr_list, date)
    print("Fetched exchange rates:", exchange_rates_data)
    return exchange_rates_data

def load_data_task(**kwargs):
    ti = kwargs['ti']
    exchange_rates_data = ti.xcom_pull(task_ids='fetch_exchange_rates')
    
    sql = """
        INSERT INTO usd_exchange_rate(dt, euro, yen, inr)
        VALUES (%s, %s, %s, %s);
    """
    
    values = (
        exchange_rates_data["date"],
        exchange_rates_data["eur"],
        exchange_rates_data["jpy"],
        exchange_rates_data["inr"],
    )

    # Execute the SQL statement
    hook = PostgresHook(postgres_conn_id="currency")
    hook.run(sql, parameters=values)

    print("Data loaded into PostgreSQL")

with DAG(
    dag_id="currency_exchange_v03",
    default_args=default_args,
    description='ETL process for currency exchange data',
    schedule_interval="0 10 * * *",  # Set your desired schedule
) as dag:

    table_creation = PostgresOperator(
        task_id="create_currency_table",
        postgres_conn_id="currency",
        sql="""
            CREATE TABLE IF NOT EXISTS usd_exchange_rate (
                dt DATE PRIMARY KEY,
                euro NUMERIC(10,3),
                yen NUMERIC(10,3),
                inr NUMERIC(10,3)
            )
        """,
        )

    fetch_currency_data = PythonOperator(
        task_id='fetch_exchange_rates',
        python_callable=fetch_exchange_rates_task,
        provide_context=True,
    )

    load_currency_data = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_data_task,
        provide_context=True,
    )

    table_creation >> fetch_currency_data >> load_currency_data
