================================================
File: README.md
================================================
## What is Apache Iceberg?
Apache Iceberg is a distributed, community-driven, Apache 2.0-licensed, 100% open-source data table format that helps simplify data processing on large datasets stored in data lakes. Data engineers use Apache Iceberg because it is fast, efficient, and reliable at any scale and keeps records of how datasets change over time. Apache Iceberg offers easy integrations with popular data processing frameworks such as Apache Spark, Apache Flink, Apache Hive, Presto, and more.

## What is a transactional data lake?
A data lake is a centralized repository that allows you to store all your structured and unstructured data at any scale. A data transaction is a series of data exchanges that are conducted in a single operation. For example, when a customer withdraws money from a bank account, the bank conducts several data exchanges at the same time in one data transaction, including verifying the account has sufficient balance, verifying identity, and debiting the withdrawal from the account. A transactional data lake is a type of data lake that not only stores data at scale but also supports transactional operations and ensures that data is accurate, consistent, and allows you to track how data and data structure changes over time. These properties are collectively known as Atomicity, Consistency, Isolation, and Durability (ACID):
- Atomicity guarantees that each transaction is a single event that either succeeds or fails completely; there is no half-way status. 
- Consistency ensures that all data written is valid according to the defined rules of the data lake, ensuring that data is accurate and reliable. 
- Isolation ensures multiple transactions can occur at the same time without interfering with each other, ensuring that each transaction executes independently.
- Durability means that data is not lost or corrupted once a transaction is submitted. Data can be recovered in the event of a system failure, such as a power outage.

## What are the benefits of using Apache Iceberg?
Some of the key benefits of using Apache Iceberg for transactional data lakes include:
- Familiarity of SQL: Structured query language (SQL) is a popular query language that is frequently used in all types of applications. Data analysts and developers learn and use SQL because it integrates well with different programming languages and is also fairly easy to learn as it uses common English keywords in its statements. Apache Iceberg allows anyone who is familiar with structured query language (SQL) to build data lakes and perform most data lake operations without needing to learn a new language.
- Data Consistency: Apache Iceberg provides data consistency to ensure that any user who reads and writes to the data sees the same data. 
- Data structure: Apache Iceberg allows for easy changes to your data structure, also known as schema evolution, meaning that users can add, rename, or remove columns from a data table without disrupting the underlying data.
- Data Versioning: Apache Iceberg provides support for data versioning, which allows users to track changes to data overtime. This enables the time travel feature, which allows users to access and query historical versions of data and analyze changes to the data between updates and deletes.
- Cross-platform support: Apache Iceberg supports a variety of different storage systems and query engines, including Apache Spark, Apache Hive, and Presto. This makes it easy to use Iceberg in a variety of different data processing environments.
I- ncremental processing: Iceberg supports incremental processing, which allows users to process only the data that has changed since the last run, also known as CDC (Change Data Capture). This can help improve data processing efficiency and performance.

## What are common use cases for Apache Iceberg?
Apache Iceberg is suited for many data lake use cases, including:
- Data tables in data lakes that require frequent deletes, such as when enforcing data privacy laws.
- Data tables in data lake that require record level updates. This is helpful when your dataset requires frequent updates after data settles, for example, sales data that may change due to later events such as customer returns. Iceberg provides capabilities to update individual records without needing to republish the entire data set.
- Data tables in data lakes that have unpredictable changes, such as Slowly Changing Dimension (SCD) tables. An example of an SCD is a customer record table that includes name, location, and contact information which may change over time at unknown intervals.
- When transactions with the data lake requires guaranteed data validity, durability, and reliability, Apache Iceberg table formats can be deployed to ensure ACID transactions.
- When there is a need to go back in time to query historical versions of data to perform trend analysis, analyze changes to data over a period of time, or to restore or rollback to a previous version to correct issues.

## Who uses Apache Iceberg?
Data engineers, data administrators, data analysts, and data scientists are among the personas that use Apache Iceberg.  Data engineers and administrators can use Apache Iceberg to design and build scalable data storage systems.  Data analysts and data scientists can use Apache Iceberg to analyze large datasets efficiently. 

## Why should you choose Apache Iceberg?
Apache Iceberg offers a fast, efficient way to process large datasets at scale. It brings the following benefits:
- Open source:  Apache Iceberg is an open source project, which means that it is free to use and can be customized to meet your specific needs. It also has an active community of developers who are continually improving and adding new features to the project. 
- Scalability:  Apache Iceberg is designed to handle large datasets efficiently. It can partition and organize data across multiple nodes, which helps distribute the workload and speed up data processing. 
- Performance: Apache Iceberg has a variety of features to optimize query performance, including columnar storage and compression techniques such as predicate push down and schema evolution. 
- Flexibility:  Apache Iceberg allows you to change how your data is organized so that it can evolve over time without requiring you to rewrite your queries or rebuild your data structures. It also supports multiple data formats and data sources, which makes it easy to integrate with existing systems. 
- Reliability:  Apache Iceberg ensures data consistency and reliability through its support for transactions. You can track how data changes over time and roll-back to historical versions to help you correct issues.


================================================
File: create_env.sh
================================================
/usr/bin/python3 -m venv /usr/bin/mf_python_env
source /usr/bin/mf_python_env/bin/activate
pip install -r requirements.txt

rm -r -f mkdir /mnt/tmp/code;/mnt/tmp/code;cd /mnt/tmp/code; aws s3 cp s3://mf-code-bucket/code.zip .

mkdir /mnt/tmp/mf_python_env;/usr/bin/python3 -m venv /mnt/tmp/mf_python_env;
source /mnt/tmp/mf_python_env/bin/activate;pip3 install pandas;pip3 install mftool;cd /mnt/tmp/code/src;spark-submit --conf spark.pyspark.python='/mnt/tmp/mf_python_env' history_load.py



================================================
File: requirements.txt
================================================
pandas
pyspark
mftool

================================================
File: src/history_load.py
================================================
import pandas as pd
from mftool import Mftool
from pyspark.sql import SparkSession
from utils.common_utils import create_logger, json_reader
from utils.spark_utils import create_iceberg_db, write_to_iceberg_db, create_iceberg_table

if __name__ == '__main__':
    logger = create_logger()
    obj = Mftool()
    api_config = json_reader('config/api_config.json')
    spark = SparkSession.builder.appName("GenerateHistData").getOrCreate()
    mf_df = pd.DataFrame(columns=['date', 'nav', 'dayChange', 'scheme_code', 'fund_house', 'scheme_type',
                                  'scheme_category', 'scheme_name'])

    scheme_codes = api_config['mf_list'][:2]
    iceberg_db = api_config['mf_db']
    iceberg_table = api_config['mf_table']
    iceberg_table_schema = api_config['mf_table_schema']
    iceberg_table_path = api_config['mf_table_bucket']
    iceberg_partition_column = api_config['mf_table_partition']

    for scheme_code in scheme_codes:
        data = obj.get_scheme_historical_nav(scheme_code, as_Dataframe=True)
        data1 = obj.get_scheme_details(scheme_code)
        data['scheme_code'] = data1["scheme_code"]
        data['fund_house'] = data1["fund_house"]
        data['scheme_type'] = data1["scheme_type"]
        data['scheme_code'] = data1["scheme_code"]
        data['scheme_category'] = data1["scheme_category"]
        data['scheme_name'] = data1["scheme_name"]
        data.reset_index(inplace=True)
        mf_df = pd.concat([mf_df, data], ignore_index=True)

    create_iceberg_db(spark, iceberg_db)
    create_iceberg_table(spark, iceberg_db, iceberg_table, iceberg_table_schema, iceberg_table_path,
                         iceberg_partition_column)
    mf_df = spark.createDataFrame(mf_df)
    write_to_iceberg_db(mf_df, iceberg_db, iceberg_table)


================================================
File: src/config/api_config.json
================================================
{
  "mf-api": "https://api.mfapi.in/mf",
  "latest-api": "https://api.mfapi.in/mf/latest",
  "mf_db": "mf_db.elss",
  "mf_table": "mutual_funds",
  "mf_table_schema": [
    "date date, nav decimal(10,4), dayChange decimal(10,4), scheme_code integer, fund_house string, scheme_type string, scheme_category string,scheme_name string"
  ],
  "mf_table_partition" : "scheme_code",
  "mf_table_bucket": "mf-data-bucket"
  ,
  "mf_list": [
    "100175",
    "100614",
    "100821",
    "100865",
    "104772",
    "111569",
    "111638",
    "111710",
    "111722",
    "112323",
    "132757",
    "133385",
    "135655",
    "135784",
    "139783",
    "141862",
    "147482",
    "150156",
    "151076",
    "151164",
    "151472"
  ]
}

================================================
File: src/utils/common_utils.py
================================================
import logging
import json


def create_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


def json_reader(path):
    with open(path, 'r') as file:
        config = json.load(file)
    return config



================================================
File: src/utils/spark_utils.py
================================================
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







