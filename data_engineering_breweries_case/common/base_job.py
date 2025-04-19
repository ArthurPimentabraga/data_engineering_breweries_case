import logging, boto3
from pyspark.sql import SparkSession
from abc import ABC, abstractmethod

class BaseJob(ABC):
    def __init__(self, app_name):
        self.logger = self._initialize_logger()
        self.spark = self._initialize_spark(app_name)
        self.s3 = self._initialize_s3_client()
        self.create_mock_s3_bucket("lake")

    def _initialize_logger(self):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(self.__class__.__name__)
        return logger

    def _initialize_spark(self, app_name):
        return (
            SparkSession.builder.appName(app_name)
            .config("spark.hadoop.fs.s3a.endpoint", "http://moto-s3:5000")
            .config("spark.hadoop.fs.s3a.access.key", "mock_access_key")
            .config("spark.hadoop.fs.s3a.secret.key", "mock_secret_key")
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .getOrCreate()
        )

    def _initialize_s3_client(self):
        return boto3.client(
            "s3",
            endpoint_url="http://moto-s3:5000",
            aws_access_key_id="mock_access_key",
            aws_secret_access_key="mock_secret_key",
        )

    def list_s3_buckets(self):
        response = self.s3.list_buckets()
        buckets = [bucket["Name"] for bucket in response.get("Buckets", [])]
        self.logger.info(f"Buckets existentes: {buckets}")
        return buckets

    def create_mock_s3_bucket(self, bucket_name):
        if bucket_name in self.list_s3_buckets():
            self.logger.info(f"Bucket '{bucket_name}' already exists.")
            return
        
        self.s3.create_bucket(Bucket=bucket_name)
        self.logger.info(f"Bucket '{bucket_name}' created successfully.")

    def stop_spark(self):
        self.logger.info("Stopping Spark session.")
        self.spark.stop()

    @abstractmethod
    def run(self):
        pass

    def execute(self):
        try:
            self.logger.info("Starting job execution...")
            self.run()
        finally:
            self.logger.info("Stopping Spark session.")
            self.spark.stop()