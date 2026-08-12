# timely-asp - redesign for DataRobot + Databricks

This repository contains the redesign for timely-asp where model inference moves to DataRobot and Databricks becomes the canonical storage and processing platform. S3 remains the source for raw inputs and intermediate artifacts. An EC2-based secure agent orchestrates scheduled tasks and job triggers.

Goals:
- Replace FastAPI-based inference with DataRobot deployments for model serving.
- Use Databricks (Delta Lake) to store ingested data and inference outputs.
- Use AWS S3 as raw data storage and transfer medium.
- Run a secure, least-privileged agent on EC2 to orchestrate jobs and interact with services.

High-level branches and artifacts are available on branch `redesign/datarobot-databricks`.

See docs/ARCHITECTURE.md for full design and docs/RUNBOOK.md for deployment steps.
