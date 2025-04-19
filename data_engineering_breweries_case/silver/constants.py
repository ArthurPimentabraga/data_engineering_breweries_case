SOURCE_CONFIG = {
    "path": "s3a://lake/bronze/",
    "format": "json"
}

SINK_CONFIG = {
    "path": "s3a://lake/silver/",
    "format": "delta",
    "partition_by": "country_partition",
    "mode": "overwrite"
}