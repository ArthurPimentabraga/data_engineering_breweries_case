import requests, time, argparse, json
from pyspark.sql import functions as f
from data_engineering_breweries_case.common.base_job import BaseJob
from data_engineering_breweries_case.bronze.constants import SOURCE_CONFIG, RESPONSE_SCHEMA, SINK_CONFIG, ENV_CONFIG
from data_engineering_breweries_case.common.utils import format_column_partition


class BronzeJob(BaseJob):
    def __init__(self, env_config=ENV_CONFIG, custom_args: dict = None):
        super().__init__(app_name="BronzeJob", env_config=env_config)
        self.custom_args = custom_args


    def _get_total_of_pages(self, total_of_breweries: int) -> int:
        """
        Calculate the total number of data pages based on the total number of breweries.
        Each page contains 200 breweries.

        Args:
            total_of_breweries (int): The total number of breweries in API.
        Returns:
            int: The total number of pages.
        """
        if total_of_breweries % 200 == 0:
            return (total_of_breweries // 200) + 1
        
        return (total_of_breweries // 200) + 2


    def _get_source_data(self) -> list:
        """
        Get data from the source API for all data pages that exist in the API

        returns:
            list: A list of dictionaries containing the brewery data.
        """
        source_data = []

        total_of_pages = self._get_total_of_pages(self.custom_args['brewery_metadata']['total'])

        for page in range(1, total_of_pages):
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
            self._save(df)
        else:
            raise Exception("Empty response from API!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process custom arguments.")
    parser.add_argument("--custom_args", type=str, required=True, help="Custom parameter for BronzeJob")
    args = parser.parse_args()
    custom_args = json.loads(args.custom_args)
    job = BronzeJob(custom_args=custom_args)
    job.execute()