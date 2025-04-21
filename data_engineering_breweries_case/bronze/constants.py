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
    sparkTypes.StructField("longitude", sparkTypes.DoubleType(), True),
    sparkTypes.StructField("latitude", sparkTypes.DoubleType(), True),
    sparkTypes.StructField("phone", sparkTypes.StringType(), True),
    sparkTypes.StructField("website_url", sparkTypes.StringType(), True),
    sparkTypes.StructField("address_1", sparkTypes.StringType(), True),
    sparkTypes.StructField("address_2", sparkTypes.StringType(), True),
    sparkTypes.StructField("address_3", sparkTypes.StringType(), True),
    sparkTypes.StructField("state_province", sparkTypes.StringType(), True)
])


SINK_CONFIG = {
    "partition_by": "country_partition",
    "path": "s3a://lake/bronze/"
}

ENV_CONFIG = {
    "s3a_endpoint": "http://moto-s3:5000"
}

ENV_CONFIG_TEST = {
    "s3a_endpoint": "http://127.0.0.1:5000"
}