from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

# Define default_args dictionary to configure your DAG
default_args = {
    'owner': 'sajal',
    'start_date': datetime(2023, 12, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id = 'postgres_dag_v03',
    default_args=default_args,
    description='connecting to postgres',
    # schedule_interval="0,5,10,15,20,25,30,35,40,45,50,55 * * * *",  # Set your desired schedule
    schedule_interval="0 0 * * *"
) as dag:
    
    task1 = PostgresOperator(
        task_id = "create_postgres_table",
        postgres_conn_id = "postgres_localhost",
        sql = """
            create table if not exists dag_runs (
                dt date,
                dag_id character varying,
                primary key (dt, dag_id)
            )
        """
    )

    task2 = PostgresOperator(
        task_id = "insert_into_postgres_table",
        postgres_conn_id = "postgres_localhost",
        sql = """
            insert into dag_runs(dt, dag_id) values ( '{{ ds }}', '{{ dag.dag_id }}');
        """
    )

    task3 = PostgresOperator(
        task_id = "delete_from_postgres_table",
        postgres_conn_id = "postgres_localhost",
        sql = """
            delete from dag_runs where dt = '{{ ds }}' and dag_id = '{{ dag.dag_id }}';
        """
    )

    task1 >> task3 >> task2
    
