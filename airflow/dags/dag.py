from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from datetime import datetime, timedelta
from airflow.utils.trigger_rule import TriggerRule
from dag_utils import get_breweries_metadata

default_args = {
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
}

with DAG(
    dag_id="data_engineering_breweries_case",
    description="Extract breweries data from API and load into S3",
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval="0 1 * * *",
    max_active_runs=1,
    catchup=False,
    tags=['s3', 'api']
) as dag:

    get_breweries_metadata_operator = PythonOperator(
        task_id="get_breweries_metadata",
        python_callable=get_breweries_metadata,
        provide_context=True,
    )

    bronze = BashOperator(
        task_id="source_to_bronze",
        bash_command=(
            "source /opt/airflow/venv/bin/activate && "
            "spark-submit --master local[*] --deploy-mode client "
            "/opt/airflow/data_engineering_breweries_case/bronze/job.py "
            "--custom_args '{{ {'brewery_metadata': ti.xcom_pull(task_ids='get_breweries_metadata')} | tojson }}'"
        ),
    )

    silver = BashOperator(
        task_id="bronze_to_silver",
        trigger_rule=TriggerRule.ALL_SUCCESS,
        bash_command=(
            "source /opt/airflow/venv/bin/activate && "
            "spark-submit --master local[*] --deploy-mode client "
            "/opt/airflow/data_engineering_breweries_case/silver/job.py"
        ),
    )

    gold = BashOperator(
        task_id="silver_to_gold",
        trigger_rule=TriggerRule.ALL_SUCCESS,
        bash_command=(
            "source /opt/airflow/venv/bin/activate && "
            "spark-submit --master local[*] --deploy-mode client "
            "/opt/airflow/data_engineering_breweries_case/gold/job.py"
        ),
    )

    get_breweries_metadata_operator >> bronze >> silver >> gold