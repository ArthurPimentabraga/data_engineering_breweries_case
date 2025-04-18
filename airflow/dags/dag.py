from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


with DAG(
    dag_id="bronze_job_dag",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    pyspark_task_2 = BashOperator(
        task_id="run_pyspark_job_2",
        bash_command=(
            "source /opt/airflow/venv/bin/activate && "
            "spark-submit --master local[*] /opt/airflow/data_engineering_breweries_case/bronze/job.py"
        ),
    )