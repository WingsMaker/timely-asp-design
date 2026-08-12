"""
Orchestration script to run a simple batch inference: read a small batch from S3, call DataRobot, and write predictions back to S3.

This script is intentionally simple and safe to run from EC2. For production-batch inference, prefer running inside Databricks where Delta tables and compute are available.
"""
import os
import json
import boto3
from datarobot_client import DataRobotClient

S3_BUCKET = os.getenv("S3_PREDICTIONS_BUCKET")
S3_PREFIX = os.getenv("S3_PREDICTIONS_PREFIX", "predictions/")
DATAROBOT_DEPLOYMENT_ID = os.getenv("DATAROBOT_DEPLOYMENT_ID")

s3 = boto3.client("s3")


def load_sample_from_s3(bucket, key):
    obj = s3.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read()
    return json.loads(body)


def write_predictions_to_s3(bucket, key, data):
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(data).encode("utf-8"))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run batch inference using DataRobot (simple runner).")
    parser.add_argument("--input-s3-key", required=True, help="S3 key to input JSON lines or JSON payload")
    parser.add_argument("--output-s3-key", required=False, help="S3 key to write predictions")
    args = parser.parse_args()

    if not DATAROBOT_DEPLOYMENT_ID:
        raise SystemExit("DATAROBOT_DEPLOYMENT_ID env var is required")

    data = load_sample_from_s3(S3_BUCKET, args.input_s3_key)
    client = DataRobotClient()
    resp = client.predict(DATAROBOT_DEPLOYMENT_ID, data)

    out_key = args.output_s3_key or (S3_PREFIX.rstrip("/") + "/predictions.json")
    write_predictions_to_s3(S3_BUCKET, out_key, resp)
    print(f"Wrote predictions to s3://{S3_BUCKET}/{out_key}")
