import pytest
from pyspark.sql.functions import  *
from pyspark.sql.types import *
from project_name.transformations.generateTax import *





def test_generating_tax(spark_test_session):
    test_data = [(23.43,), (2.343,), (234.3,)]
    test_data_df = spark_test_session.createDataFrame(
        test_data,
        ["cost"])
    expected_data = [(23.43, 3), (2.343, 0), (234.3, 35)]
    expected_df = spark_test_session.createDataFrame(expected_data, ["cost", "tax"])
    expected = expected_df.orderBy("cost").collect()
    tax = udf(taxCol,IntegerType())
    output_df = test_data_df.withColumn("tax",tax(col('cost')))
    output = output_df.orderBy("cost").collect()
    assert output == expected