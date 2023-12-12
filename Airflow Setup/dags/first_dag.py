from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Define default_args dictionary to configure your DAG
default_args = {
    'owner': 'sajal',
    'start_date': datetime(2023, 12, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate a DAG using the with statement
with DAG(
    'my_first_dag_v02',
    default_args=default_args,
    description='A simple data pipeline',
    schedule_interval=timedelta(days=1),  # Set your desired schedule
) as dag:

    # Define tasks within the DAG context
    def extract_data(**kwargs):
        # Your code for extracting data
        print("Extracting data at ", datetime.now())

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_data,
        provide_context=True,  # Pass the context to the callable function
    )

    def transform_data(**kwargs):
        # Your code for transforming data
        print("Transforming data")

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_data,
        provide_context=True,
    )

    def load_data(**kwargs):
        # Your code for loading data
        print("Loading data")

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load_data,
        provide_context=True,
    )

    # Set up task dependencies
    extract_task >> transform_task >> load_task
