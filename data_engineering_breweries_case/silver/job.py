from data_engineering_breweries_case.common.base_job import BaseJob
from pyspark.sql import functions as f
from constants import SOURCE_CONFIG, SINK_CONFIG
from pyspark.sql import DataFrame


class SilverJob(BaseJob):
    def __init__(self):
        super().__init__(app_name="SilverJob")

    def _get_source_data(self) -> DataFrame:
        return self.spark.read.format(SOURCE_CONFIG["format"]).load(SOURCE_CONFIG["path"])

    def _save(self, df:DataFrame):
        (
            df.write.format(SINK_CONFIG["format"])
            .mode(SINK_CONFIG["mode"])
            .save(SINK_CONFIG["path"])
        )

        self.spark.sql(f"OPTIMIZE '{SINK_CONFIG['path']}' ZORDER BY (city)")

    def run(self):
        df = self._get_source_data()
        df.show()
        self._save(df)


if __name__ == "__main__":
    job = SilverJob()
    job.execute()