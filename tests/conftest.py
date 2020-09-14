import pytest
from helix.SparkSessionBuilder import getSession


@pytest.fixture(scope="session")
def spark_test_session():
    spark,log     = getSession.startSpark(hiveSupport=False)
    return (spark)
