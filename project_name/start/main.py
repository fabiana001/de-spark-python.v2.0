from helix.SparkSessionBuilder import getSession
from helix.AccumLogger import builder,logger
from helix.Config import typeSafe
from pyspark.sql.functions import *
from pyspark.sql.types import *
import argparse
from project_name.transformations.generateTax import *


def extract(spark,log,configs):
    log.info("loading Customers data")
    customers = spark.read.parquet(configs['data']['customers'])
    log.info("loading Orders data")
    orders    = spark.read.parquet(configs['data']['orders'])
    return customers,orders


def transform(customers,log):
    log.info("Doing a custom transformation")
    log.info("Generating tax for customers")
    tax = udf(taxCol,IntegerType())  
    customers = customers.withColumn("tax",tax(col('cost')))
    log.info("tax generated")
    return customers
    
def load(customers):
    customers.show()


def main(configFile,region):
    configs =  typeSafe.parseConfig(configFile,convertToJson=True)[region]
    spark_Configs = configs['spark_config']
    spark,log     = getSession.startSpark(spark_configs=spark_Configs,hiveSupport=False)
    log.info("Starting job")
    customers,orders =  extract(spark,log,configs)
    customers=transform(customers,log)
    load(customers)
    log.info("job completed")


#if __name__ == '__main__':
#    parser = argparse.ArgumentParser(description='Pyspark Job Arguments')
#    parser.add_argument("--region",type=str)
#    parser.add_argument("--configFile",type=str)
#    args    = parser.parse_args()
#    configs =  typeSafe.parseConfig(args.configFile,convertToJson=True)[args.region]
#    main(configs)
    
if __name__ == '__main__':
    sys.exit(main(configFile,region))
    
