import os
import glob

from pyspark.sql.functions import col
from pyspark.sql import functions as F
from pyspark.sql import SparkSession, DataFrame


def main():
    """Main ETL script definition."""
    input_path = os.getenv("INPUT_DATA_PATH", "data/*.csv")
    output_dir = os.getenv("OUTPUT_DATA_PATH", "best_daily")

    spark = (
        SparkSession.builder.appName("testApp")
        .master(os.getenv("SPARK_MASTER_URL"))
        .config("spark.hadoop.fs.s3a.endpoint", os.getenv("AWS_S3_ENDPOINT_URL"))
        .config("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID"))
        .config("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY"))
        .config("spark.hadoop.fs.s3a.fast.upload", True)
        .config("spark.hadoop.fs.s3a.path.style.access", True)
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .getOrCreate()
    )

    data = extract_data(spark, input_path)
    data_transformed = transform_data(data)
    load_data(data_transformed, output_dir)

    spark.stop()


def extract_data(spark: SparkSession, path: str) -> DataFrame:
    """Loads all csv found in path arg and put it in a dataframe
    Assumes same columns for every csv

    Returns:
        [spark.Dataframe]: appended coins csvs
    """
    files = glob.glob(path)
    schema = spark.read.csv(files[0], header=True).schema
    df = spark.createDataFrame(data=spark.sparkContext.emptyRDD(), schema=schema)

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
    df = df.withColumn(
        "closing_position", F.when(col("Close") > col("Open"), True).otherwise(False)
    )
    df = df.withColumn("daily_diff", df["Close"] - df["Open"])
    df = df.withColumn(
        "daily_diff_percentage", ((df["Close"] - df["Open"]) / df["Open"]) * 100
    )
    df_daily_best = df.sort("Date", "daily_diff_percentage").dropDuplicates(["Date"])

    return df_daily_best


def load_data(df: DataFrame, output_dir: str) -> DataFrame:
    """Save file to disk

    Args:
        df (spark.DataFrame): Undergone the transformation
        output_dir (str): Output directory where files will be written
    """
    bucket = os.getenv("AWS_S3_BUCKET")
    df.coalesce(1).write.csv(
        f"s3a://{bucket}/{output_dir}", mode="overwrite", header=True
    )


if __name__ == "__main__":
    main()
