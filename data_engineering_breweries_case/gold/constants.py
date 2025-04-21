SOURCE_CONFIG = {
    "path": "s3a://lake/silver/",
    "format": "delta"
}

SINK_CONFIG = {
    "path": "s3a://lake/gold/",
    "format": "delta",
    "partition_by": "country_partition",
    "mode": "overwrite"
}

ENV_CONFIG = {
    "s3a_endpoint": "http://moto-s3:5000"
}

ENV_CONFIG_TEST = {
    "s3a_endpoint": "http://127.0.0.1:5000"
}