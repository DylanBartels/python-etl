import os
import glob

from pyspark.sql.functions import col
from pyspark.sql import functions as F
from pyspark.sql import SparkSession, DataFrame


def main():
    """Main ETL script definition."""
    spark = SparkSession.builder.appName("testApp").master(os.getenv("SPARK_MASTER_URL")).getOrCreate()
    data = extract_data(spark, os.getenv("INPUT_DATA_PATH", "data/*.csv"))
    data_transformed = transform_data(data)
    load_data(data_transformed, os.getenv("OUTPUT_DATA_PATH", 'best_daily'))
    
    spark.stop()


def extract_data(spark: SparkSession, path: str) -> DataFrame:
    """Loads all csv found in path arg and put it in a dataframe
    Assumes same columns for every csv

    Returns:
        [spark.Dataframe]: appended coins csvs
    """
    files = glob.glob(path)
    schema = spark.read.csv(files[0], header=True).schema
    df = spark.createDataFrame(data = spark.sparkContext.emptyRDD(), schema = schema)

    for file in files:
        df_csv = spark.read.csv(file, header=True)
        df = df.union(df_csv)

    return df


def transform_data(df: DataFrame) -> DataFrame:
    """Create new dataframe with historical daily best performing coin

    Args:
        df (spark.DataFrame): all coins historical data

    Returns:
        [spark.DataFrame]: dataframe with daily best performer
    """
    df = df.withColumn("Date", df["Date"].cast("date"))
    df = df.withColumn("closing_position", F.when(col("Close") > col("Open"), True).otherwise(False))
    df = df.withColumn("daily_diff", df["Close"] - df["Open"])
    df = df.withColumn("daily_diff_percentage", ((df["Close"] - df["Open"]) / df["Open"]) * 100)
    df_daily_best = df.sort("Date","daily_diff_percentage").dropDuplicates(["Date"])

    return df_daily_best


def load_data(df: DataFrame, file_name: str) -> DataFrame:
    """Save file to disk

    Args:
        df (spark.DataFrame): Undergone the transformation
        file_name (str): Outputfile name
    """
    df.write.csv(file_name, mode='overwrite', header=True)


if __name__ == '__main__':
    main()