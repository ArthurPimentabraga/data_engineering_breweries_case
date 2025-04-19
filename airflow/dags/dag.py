from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from datetime import datetime, timedelta

default_args = {
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
}

with DAG(
    dag_id="data_engineering_breweries_case",
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    bronze = BashOperator(
        task_id="source_to_bronze",
        bash_command=(
            "source /opt/airflow/venv/bin/activate && "
            "spark-submit --master local[*] --deploy-mode client "
            "/opt/airflow/data_engineering_breweries_case/bronze/job.py"
        ),
    )

    silver = BashOperator(
        task_id="bronze_to_silver",
        bash_command=(
            "source /opt/airflow/venv/bin/activate && "
            "spark-submit --master local[*] --deploy-mode client "
            "/opt/airflow/data_engineering_breweries_case/silver/job.py"
        ),
    )

    bronze >> silver