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