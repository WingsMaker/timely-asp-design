# Security notes

Secrets & tokens
- Never commit API keys, tokens, or passwords to this repository.
- Recommended placement of secrets:
  - Databricks Secret Scopes: for jobs that run inside Databricks (preferred for Databricks-based batch inference).
  - AWS Secrets Manager: for secrets used by EC2 agent if you prefer AWS-native storage.

IAM & least privilege
- EC2 instance role: grant only S3 read access to the input buckets, and S3 write only to a dedicated staging prefix (if EC2 will write predictions). Attach no broad admin permissions.
- Databricks job/service principal: grant limited access to required Delta tables and DBFS paths.

Network
- Use VPC endpoints to restrict S3 access to the VPC where Databricks/EC2 run.
- Lock down EC2 security groups to only allow operator SSH (or better: disable SSH and use SSM) and egress to Databricks endpoints.

Auditing
- Enable CloudTrail and Databricks audit logs for job runs and secret usage monitoring.
