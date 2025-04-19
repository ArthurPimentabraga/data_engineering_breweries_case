from pyspark.sql import functions as f

def format_column_partition(column_name: str) -> str:
    return f.regexp_replace(f.lower(f.col(column_name)), " ", "_")