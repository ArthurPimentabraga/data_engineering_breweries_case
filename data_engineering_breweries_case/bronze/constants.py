import pyspark.sql.types as sparkTypes

SOURCE_CONFIG = {
    "url": "https://api.openbrewerydb.org/v1/breweries",
    "headers": {
        "Content-Type": "application/json"
    }
}

RESPONSE_SCHEMA = sparkTypes.StructType([
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

SINK_CONFIG = {
    "partition_by": "country_partition",
    "path": "s3a://lake/data/bronze/"
}