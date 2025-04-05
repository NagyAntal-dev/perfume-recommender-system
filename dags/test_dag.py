from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'test_dag',
    default_args=default_args,
    description='A simple test DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 4, 1),
    catchup=False,
    tags=['example'],
) as dag:

    print_date = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    sleep = BashOperator(
        task_id='sleep',
        bash_command='sleep 5',
    )

    print_date >> sleep
