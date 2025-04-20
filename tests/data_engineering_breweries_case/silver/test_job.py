from moto import mock_aws
from data_engineering_breweries_case.silver.job import SilverJob
from unittest.mock import patch
from data_engineering_breweries_case.silver.constants import ENV_CONFIG_TEST
import pytest
from tests.common.constants import MOCK_DATA, FULL_SCHEMA


def _run_job():
    job = SilverJob(env_config=ENV_CONFIG_TEST)
    job.run()

@pytest.fixture(autouse=True)
def mock_http_request(create_spark_session):
    df_mock = create_spark_session.createDataFrame(MOCK_DATA, schema=FULL_SCHEMA)
    with patch("data_engineering_breweries_case.silver.job.SilverJob._get_source_data", return_value=df_mock) as mock_method:
        yield mock_method

@mock_aws
def test_one(create_spark_session, moto_server):
    pass
