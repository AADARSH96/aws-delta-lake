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
