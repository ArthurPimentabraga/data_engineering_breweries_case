from data_engineering_breweries_case.common.base_job import BaseJob
from pyspark.sql import functions as f
from data_engineering_breweries_case.silver.constants import SOURCE_CONFIG, SINK_CONFIG, ENV_CONFIG
from pyspark.sql import DataFrame


class SilverJob(BaseJob):
    def __init__(self, env_config=ENV_CONFIG):
        super().__init__(app_name="SilverJob", env_config=env_config)

    def _get_source_data(self) -> DataFrame:
        return self.spark.read.format(SOURCE_CONFIG["format"]).load(SOURCE_CONFIG["path"])

    def _save(self, df:DataFrame):
        (
            df.write.format(SINK_CONFIG["format"])
            .mode(SINK_CONFIG["mode"])
            .partitionBy(SINK_CONFIG["partition_by"])
            .save(SINK_CONFIG["path"])
        )

        self.spark.sql(f"OPTIMIZE '{SINK_CONFIG['path']}' ZORDER BY (city)")

    def run(self):
        df = self._get_source_data()
        self._save(df)

if __name__ == "__main__":
    job = SilverJob()
    job.execute()