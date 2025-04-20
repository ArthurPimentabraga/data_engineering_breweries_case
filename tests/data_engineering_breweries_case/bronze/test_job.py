from moto import mock_aws
from data_engineering_breweries_case.bronze.job import BronzeJob
from unittest.mock import patch
from data_engineering_breweries_case.bronze.constants import ENV_CONFIG_TEST
import pytest
import pyspark.sql.types as sparkTypes
from tests.common.constants import SOURCE_DATA, FULL_SCHEMA


def _run_job():
    job = BronzeJob(env_config=ENV_CONFIG_TEST)
    job.run()

@pytest.fixture(autouse=True)
def mock_http_request():
    with patch("data_engineering_breweries_case.bronze.job.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = SOURCE_DATA
        yield mock_get

@mock_aws
def test_should_have_partition_column_in_correct_form(create_spark_session, moto_server):
    _run_job()
    df_output = create_spark_session.read.format("json").load("s3a://lake/bronze/")

    column_partition_value = df_output.first()["country_partition"]

    assert " " not in column_partition_value
    assert column_partition_value.islower()


@mock_aws
def test_should_have_expected_schema(create_spark_session, moto_server):
    _run_job()
    df_output = create_spark_session.read.format("json").load("s3a://lake/bronze/")
    assert df_output.schema == FULL_SCHEMA
