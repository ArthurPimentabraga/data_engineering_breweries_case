import os, pytest
from moto.server import ThreadedMotoServer
from pyspark.sql import SparkSession

@pytest.fixture()
def create_spark_session():
    spark = (
        SparkSession.builder.appName("test")
            .config("spark.hadoop.fs.s3a.endpoint", "http://127.0.0.1:5000")
            .config("spark.hadoop.fs.s3a.access.key", "mock_access_key")
            .config("spark.hadoop.fs.s3a.secret.key", "mock_secret_key")
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.jars", f"{get_spark_home_path()}/jars/delta-core_2.12-2.4.0.jar,{get_spark_home_path()}/jars/delta-storage-2.4.0.jar")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore")
        .getOrCreate()
    )
    yield spark
    spark.stop()


def get_spark_home_path() -> str:
    """
    Get the path to the Spark home directory.
    """
    spark_home = os.environ.get("SPARK_HOME")
    if not spark_home:
        raise EnvironmentError("SPARK_HOME environment variable is not set.")
    print(f"Spark home path: {spark_home}")
    return spark_home


@pytest.fixture()
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "mock_access_key"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "mock_secret_key"


@pytest.fixture()
def moto_server(aws_credentials):
    moto_server = ThreadedMotoServer(port=5000)
    moto_server.start()
    yield 
    moto_server.stop()