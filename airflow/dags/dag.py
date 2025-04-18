from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


with DAG(
    dag_id="data_engineering_breweries_case",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    bronze = BashOperator(
        task_id="source_to_bronze",
        bash_command=(
            "source /opt/airflow/venv/bin/activate && "
            "spark-submit --master local[*] /opt/airflow/data_engineering_breweries_case/bronze/job.py"
        ),
    )