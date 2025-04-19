SOURCE_CONFIG = {
    "path": "s3a://lake/data/bronze/",
    "format": "json"
}

SINK_CONFIG = {
    "path": "s3a://lake/data/silver/",
    "format": "delta",
    "partition_by": "country_partition",
    "mode": "overwrite"
}