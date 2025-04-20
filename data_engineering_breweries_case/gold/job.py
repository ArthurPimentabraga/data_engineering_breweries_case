from data_engineering_breweries_case.common.base_job import BaseJob
from pyspark.sql import functions as f
from data_engineering_breweries_case.gold.constants import SOURCE_CONFIG, SINK_CONFIG, ENV_CONFIG
from pyspark.sql import DataFrame
from data_engineering_breweries_case.common.utils import format_column_partition


class GoldJob(BaseJob):
    def __init__(self, env_config=ENV_CONFIG):
        super().__init__(app_name="GoldJob", env_config=env_config)

    def _get_source_data(self) -> DataFrame:
        return self.spark.read.format(SOURCE_CONFIG["format"]).load(SOURCE_CONFIG["path"])

    def _save(self, df:DataFrame):
        (
            df.write.format(SINK_CONFIG["format"])
            .mode(SINK_CONFIG["mode"])
            .partitionBy(SINK_CONFIG["partition_by"])
            .save(SINK_CONFIG["path"])
        )

    def _aggregate_brewery_data(self, df: DataFrame) -> DataFrame:
        return(
            df.groupBy("brewery_type", "country").agg(
                f.count("*").alias("quantity_breweries"),
            ).select(
                f.col("brewery_type"),
                f.col("country"),
                f.col("quantity_breweries"),
                format_column_partition("country").alias(SINK_CONFIG["partition_by"]),
            )
        )

    def run(self):
        df = self._get_source_data()

        df_aggregated = self._aggregate_brewery_data(df)
        df_aggregated.show(truncate=False, n=20)

        self._save(df_aggregated)


if __name__ == "__main__":

    job = GoldJob()
    job.execute()