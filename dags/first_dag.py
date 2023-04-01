from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'my_dag',
    default_args=default_args,
    description='A simple DAG that runs a Python script',
    schedule_interval=timedelta(days=1),
)

def my_function():
    print('Hello, world!')

run_my_function = PythonOperator(
    task_id='run_my_function',
    python_callable=my_function,
    dag=dag,
)

run_my_function

