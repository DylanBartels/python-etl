import os
import glob

import prefect
import numpy as np
import pandas as pd

from s3fs.core import S3FileSystem
from prefect import Flow, task

logger = prefect.context.get("logger")


@task
def extract(path: str):
    """Loads all csv found in path arg and put it in a dataframe
    Assumes same columns for every csv

    Returns:
        [pd.Dataframe]: appended coins csvs
    """
    files = glob.glob(path)
    df = pd.DataFrame()

    for file in files:
        df_csv = pd.read_csv(file)
        df = df.append(df_csv)

    logger.info(f"Shape of the dataframe is: {df.shape}")
    return df.reset_index(drop=True)


@task
def transform(df: pd.DataFrame):
    """Create new dataframe with historical daily best performing coin

    Args:
        df (pd.DataFrame): all coins historical data

    Returns:
        [pd.DataFrame]: dataframe with daily best performer
    """
    df["Date"] = pd.to_datetime(df.loc[:, "Date"], utc=True)
    df["closing_positive"] = np.where(df["Close"] > df["Open"], True, False)
    df["daily_diff"] = df["Close"] - df["Open"]
    df["daily_diff_percentage"] = ((df["Close"] - df["Open"]) / df["Open"]) * 100

    df_daily_best = (
        df.sort_values(["Date", "daily_diff_percentage"], ascending=[False, False])
        .drop_duplicates(["Date"])
        .reset_index(drop=True)
    )

    return df_daily_best



@task
def load_data(df: pd.DataFrame, file_name: str):
    """Upload data to s3

    Args:
        df (pd.DataFrame): Undergone the transformation
        file_name (str): Outputfile name
    """
    s3 = S3FileSystem(
        anon=False,
        client_kwargs={
            "endpoint_url": os.getenv("AWS_S3_ENDPOINT_URL"),
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        },
    )
    bytes_to_write = df.to_csv(None).encode()
    with s3.open(f"s3://{os.getenv('AWS_S3_BUCKET')}/{file_name}.csv", "wb") as f:
        f.write(bytes_to_write)


with Flow("etl-example") as flow:
    df = extract("data/*.csv")
    df_daily_best = transform(df)
    load_data(df_daily_best, "best_daily")
