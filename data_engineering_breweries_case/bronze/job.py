import logging, requests
from pyspark.sql import SparkSession
import pyspark.sql.types as sparkTypes
from pyspark.sql import functions as f

config = {
    "url": "https://api.openbrewerydb.org/v1/breweries",
    "headers": {
        "Content-Type": "application/json"
    }
}


class BronzeJob:
    def __init__(self):
        pass

    def run(self): # TODO Dividir em métodos
        # TODO Passar o spark session e o logger para classe mãe

        spark = SparkSession.builder.appName("BronzeJob").getOrCreate()

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        response = requests.get(config["url"], headers=config["headers"])

        if response.status_code == 200:
            logger.info("Request successful")
            data = response.json()

            # TODO Se não tiver dados, falhar?

            schema = sparkTypes.StructType([
                sparkTypes.StructField("id", sparkTypes.StringType(), True),
                sparkTypes.StructField("name", sparkTypes.StringType(), True),
                sparkTypes.StructField("brewery_type", sparkTypes.StringType(), True),
                sparkTypes.StructField("street", sparkTypes.StringType(), True),
                sparkTypes.StructField("city", sparkTypes.StringType(), True),
                sparkTypes.StructField("state", sparkTypes.StringType(), True),
                sparkTypes.StructField("postal_code", sparkTypes.StringType(), True),
                sparkTypes.StructField("country", sparkTypes.StringType(), True),
                sparkTypes.StructField("longitude", sparkTypes.FloatType(), True),
                sparkTypes.StructField("latitude", sparkTypes.FloatType(), True),
                sparkTypes.StructField("phone", sparkTypes.StringType(), True),
                sparkTypes.StructField("website_url", sparkTypes.StringType(), True)
            ])

            df = spark.createDataFrame(data, schema=schema)

            df = df.withColumns({
                "country_partition": f.regexp_replace(f.lower(f.col("country")), " ", "_")
            })

            df.show(truncate=False, n=5)
        else:
            logger.error(
                f"Request failed with status code {response.status_code}"
                f" and message: {response.text}"
            )
            # TODO Deixar falhar?

        spark.stop()


if __name__ == "__main__":
    job = BronzeJob()
    job.run()