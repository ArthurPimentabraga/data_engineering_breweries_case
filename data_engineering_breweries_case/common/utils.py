from pyspark.sql import functions as f

def format_column_partition(column_name: str) -> str:
    """
    Format a column value to be used as a partition in a DataFrame.
    This function replaces spaces with underscores and converts the column value to lowercase.

    Args:
        column_name (str): The name of the column to format.
    Returns:
        str: The formatted column.
    """
    return f.regexp_replace(f.lower(f.col(column_name)), " ", "_")