from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from data_engineering_breweries_case.bronze.job import BronzeJob


def run_bronze_job():
    job = BronzeJob()
    job.run()


with DAG(
    dag_id="bronze_job_dag",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    bronze_job_task = PythonOperator(
        task_id="run_bronze_job",
        python_callable=run_bronze_job,
    )