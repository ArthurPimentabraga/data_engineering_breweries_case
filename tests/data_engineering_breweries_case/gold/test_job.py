from moto import mock_aws
from data_engineering_breweries_case.gold.job import GoldJob
from unittest.mock import patch
from data_engineering_breweries_case.gold.constants import ENV_CONFIG_TEST
import pytest
from tests.common.constants import MOCK_DATA, FULL_SCHEMA, GOLD_SCHEMA


def _run_job():
    job = GoldJob(env_config=ENV_CONFIG_TEST)
    job.run()

@pytest.fixture(autouse=True)
def mock_source_data(create_spark_session):
    df_mock = create_spark_session.createDataFrame(MOCK_DATA, schema=FULL_SCHEMA)
    with patch("data_engineering_breweries_case.gold.job.GoldJob._get_source_data", return_value=df_mock) as mock_method:
        yield mock_method

@mock_aws
def test_should_only_have_one_record_per_combination_of_country_and_brewery_type(create_spark_session, moto_server):
    _run_job()
    
    df_output = create_spark_session.read.format("delta").load("s3a://lake/gold/")
    df_filtered_first_agg = df_output.filter("country = 'Country 1' and brewery_type = 'micro'")
    df_filtered_second_agg = df_output.filter("country = 'Country 1' and brewery_type = 'large'")
    
    assert df_filtered_first_agg.count() == 1
    assert df_filtered_second_agg.count() == 1


@mock_aws
def test_quantity_breweries_should_match_records_per_country_and_type(create_spark_session, moto_server):
    _run_job()
    
    df_output = create_spark_session.read.format("delta").load("s3a://lake/gold/")
    quantity_breweries_first_agg = (
        df_output.filter("country = 'Country 1' and brewery_type = 'micro'")
        .collect()[0]["quantity_breweries"]
    )
    quantity_breweries_second_agg = (
        df_output.filter("country = 'Country 1' and brewery_type = 'large'")
        .collect()[0]["quantity_breweries"]
    )
    
    assert quantity_breweries_first_agg == 2
    assert quantity_breweries_second_agg == 1


@mock_aws
def test_should_have_expected_schema(create_spark_session, moto_server):
    _run_job()
    df_output = create_spark_session.read.format("delta").load("s3a://lake/gold/")
    assert df_output.schema == GOLD_SCHEMA
