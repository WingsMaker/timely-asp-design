from pyspark.sql import SparkSession
import os

def read_from_s3_and_write_delta(s3_path: str, delta_path: str):
    """Read Parquet/CSV from S3 and write to a Delta path.
    Run this on Databricks (recommended) where Spark is configured and Delta is available.
    """
    spark = SparkSession.builder.getOrCreate()
    # Auto-detect format if desired; here we assume Parquet for performance.
    df = spark.read.format("parquet").load(s3_path)

    # Example: data validation or transformations would go here
    # df = df.dropna(subset=[...])

    df.write.format("delta").mode("append").save(delta_path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--s3-path", required=True)
    parser.add_argument("--delta-path", required=True)
    args = parser.parse_args()

    read_from_s3_and_write_delta(args.s3_path, args.delta_path)
