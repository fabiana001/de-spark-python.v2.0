from helix.SparkSessionBuilder import getSession
from helix.AccumLogger.logger import *
from helix.AccumLogger.builder import *
from helix.Config import typeSafe
from pyspark.sql.functions import *
from pyspark.sql.types import *
import argparse
from project_name.transformations.generateTax import *
from project_name.transformations.generateTax_rdd import *


def extract(spark,log,configs):
    log.info("loading Customers data")
    customers = spark.read.parquet(configs['data']['customers'])
    log.info("loading Orders data")
    orders    = spark.read.parquet(configs['data']['orders'])
    return customers,orders


def transform(customers,orders,log,metrics):
    log.info("Doing a custom transformation")
    log.info("Generating tax for orders")
    # Run UDF function on orders
    tax     = udf(taxCol,IntegerType())  
    orders  = orders.withColumn("tax",tax(col('OrderValue')))
    # Run RDD map function on customers
    columns =  customers.columns+['tax']
    customers   = recordBuilder(customers.rdd,processCustomers,metrics).toDF()
    log.info("tax generated")
    log.info("Print Accum Error Log")
    return customers,orders
    
def load(customers,orders):
    customers.show()
    orders.show()


def main(configFile,region):
    configs =  typeSafe.parseConfig(configFile,convertToJson=True)[region]
    spark_Configs = configs['spark_config']
    spark,log     = getSession.startSpark(spark_configs=spark_Configs,hiveSupport=False)
    # Create a accum logger
    acc     = spark.sparkContext.accumulator(dict(),CustomAccumulator())
    metrics = MetricRegistry(acc,['id','Error Type','Error Message'],'logger')
    log.info("Starting job")
    customers,orders =  extract(spark,log,configs)
    customersT,ordersT=transform(customers,orders,log,metrics)
    load(customersT,ordersT)
    #print Errors from accumulator
    try:
        metrics.getErrorData(spark).show()
    except Exception as e:
        print(metrics.getErrorDict())
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
    
