#!/usr/bin/env python3
"""
EC2 agent skeleton: periodically runs tasks (ingest, inference) and triggers Databricks jobs when needed.

This is a minimal example. In production, consider running under a process supervisor, use SSM instead of SSH for access,
and ensure logging/metrics are shipped to CloudWatch or another monitoring system.
"""
import os
import subprocess
import time
import logging

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("ec2_agent")

# Replace with real scheduling or use systemd timers / cron
POLL_INTERVAL_SECONDS = int(os.getenv("AGENT_POLL_SECONDS", "300"))


def run_cmd(cmd: list):
    LOG.info("Running: %s", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    LOG.info("Exit %s", res.returncode)
    if res.stdout:
        LOG.info(res.stdout)
    if res.stderr:
        LOG.warning(res.stderr)
    return res.returncode == 0


def main_loop():
    while True:
        LOG.info("Agent heartbeat: checking work")
        # Example: run a scheduled inference driver that calls run_inference.py
        # Adjust the S3 key value to point to a real input payload / prefix
        input_key = os.getenv("AGENT_SAMPLE_INPUT_KEY", "sample/input.json")
        output_key = os.getenv("AGENT_SAMPLE_OUTPUT_KEY", "sample/predictions.json")

        cmd = [
            "python3",
            "/opt/timely-asp/src/inference/run_inference.py",
            "--input-s3-key",
            input_key,
            "--output-s3-key",
            output_key,
        ]
        success = run_cmd(cmd)
        if not success:
            LOG.error("Inference run failed; will retry on next cycle")

        LOG.info("Sleeping for %s seconds", POLL_INTERVAL_SECONDS)
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main_loop()
