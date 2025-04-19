import requests
from pyspark.sql import functions as f
from data_engineering_breweries_case.common.base_job import BaseJob
from bronze.constants import SOURCE_CONFIG, RESPONSE_SCHEMA, SINK_CONFIG
from data_engineering_breweries_case.common.utils import format_column_partition


class BronzeJob(BaseJob):
    def __init__(self):
        super().__init__(app_name="BronzeJob")


    def _get_source_data(self):
        return requests.get(SOURCE_CONFIG["url"], headers=SOURCE_CONFIG["headers"])


    def _create_column_partition(self, data):
        df = self.spark.createDataFrame(data, schema=RESPONSE_SCHEMA)

        return df.withColumn(
            SINK_CONFIG["partition_by"], format_column_partition("country")
        )


    def _save(self, df):
        df.coalesce(1).write.mode("overwrite").partitionBy(SINK_CONFIG["partition_by"]).json(SINK_CONFIG["path"])


    def run(self):
        response = self._get_source_data()

        if response.status_code == 200:
            self.logger.info("Request successful")
            source_data = response.json()

            df = self._create_column_partition(source_data)
            df.show(truncate=False, n=5)
            self._save(df)
        else:
            raise Exception(
                f"Request failed with status code {response.status_code}"
                f" and message: {response.text}"
            )

if __name__ == "__main__":
    job = BronzeJob()
    job.execute()