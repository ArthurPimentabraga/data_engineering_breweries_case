from moto import mock_aws
from data_engineering_breweries_case.bronze.job import BronzeJob
from unittest.mock import patch
from data_engineering_breweries_case.bronze.constants import ENV_CONFIG_TEST
import pytest
import pyspark.sql.types as sparkTypes


def _run_job():
    job = BronzeJob(env_config=ENV_CONFIG_TEST)
    job.run()

@pytest.fixture(autouse=True)
def mock_http_request():
    with patch("data_engineering_breweries_case.bronze.job.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "name": "Brewery 1",
                "brewery_type": "micro",
                "address_1": "Address 1",
                "city": "City 1",
                "state_province": "State province 1",
                "postal_code": "11111-1111",
                "country": "Country 1",
                "longitude": -11.11111111,
                "latitude": 11.11111111,
                "phone": "1111111111",
                "state": "State 1",
                "street": "Street 1"
            }
        ]
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
    
    EXPECTED_SCHEMA = sparkTypes.StructType([
        sparkTypes.StructField('address_1', sparkTypes.StringType(), True), 
        sparkTypes.StructField('brewery_type', sparkTypes.StringType(), True), 
        sparkTypes.StructField('city', sparkTypes.StringType(), True), 
        sparkTypes.StructField('country', sparkTypes.StringType(), True), 
        sparkTypes.StructField('id', sparkTypes.StringType(), True), 
        sparkTypes.StructField('latitude', sparkTypes.DoubleType(), True), 
        sparkTypes.StructField('longitude', sparkTypes.DoubleType(), True), 
        sparkTypes.StructField('name', sparkTypes.StringType(), True), 
        sparkTypes.StructField('phone', sparkTypes.StringType(), True), 
        sparkTypes.StructField('postal_code', sparkTypes.StringType(), True), 
        sparkTypes.StructField('state', sparkTypes.StringType(), True), 
        sparkTypes.StructField('state_province', sparkTypes.StringType(), True), 
        sparkTypes.StructField('street', sparkTypes.StringType(), True), 
        sparkTypes.StructField('country_partition', sparkTypes.StringType(), True)
    ])

    assert df_output.schema == EXPECTED_SCHEMA
