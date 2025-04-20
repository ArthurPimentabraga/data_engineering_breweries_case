import requests, time
from pyspark.sql import functions as f
from data_engineering_breweries_case.common.base_job import BaseJob
from data_engineering_breweries_case.bronze.constants import SOURCE_CONFIG, RESPONSE_SCHEMA, SINK_CONFIG, ENV_CONFIG
from data_engineering_breweries_case.common.utils import format_column_partition


class BronzeJob(BaseJob):
    def __init__(self, env_config=ENV_CONFIG):
        super().__init__(app_name="BronzeJob", env_config=env_config)

    def _get_source_data(self) -> list:
        source_data = []

        for page in range(1, 43):
            response = requests.get(SOURCE_CONFIG["url"], headers=SOURCE_CONFIG["headers"], params={"page": page, "per_page": 200})
            
            if response.status_code == 200:
                source_data.extend(response.json())
            else:
                raise Exception(
                    f"Request failed with status code {response.status_code}"
                    f" and message: {response.text}"
                )
            
            time.sleep(0.5)  # To avoid making API requests too quickly
            
        return source_data

    def _create_column_partition(self, data):
        df = self.spark.createDataFrame(data, schema=RESPONSE_SCHEMA)

        return df.withColumn(
            SINK_CONFIG["partition_by"], format_column_partition("country")
        )

    def _save(self, df):
        df.coalesce(1).write.mode("overwrite").partitionBy(SINK_CONFIG["partition_by"]).json(SINK_CONFIG["path"])

    def run(self):
        source_data = self._get_source_data()

        if len(source_data) > 0:
            df = self._create_column_partition(source_data)
            df.show(truncate=False, n=5)
            print(f"Number of records: {df.count()}")
            self._save(df)
        else:
            raise Exception("Empty response from API!")

if __name__ == "__main__":
    job = BronzeJob()
    job.execute()