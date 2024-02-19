import json
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType


def create_iceberg_db(spark, iceberg_db):
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {iceberg_db}")


def create_iceberg_table(spark, iceberg_db, iceberg_table, iceberg_table_schema, iceberg_table_path, partition_column):
    s3_path =
    spark.sql(f"""CREATE TABLE  {iceberg_db}.{iceberg_table} (
    {iceberg_table_schema}
    )
    USING iceberg 
    location '{s3_path}'
    PARTITIONED BY {partition_column}""")


def write_to_iceberg_db(df, iceberg_db, iceberg_table):
    df.writeTo(f"{iceberg_db}.{iceberg_table}").using("iceberg").tableProperty("format-version", "2").createOrReplace()




