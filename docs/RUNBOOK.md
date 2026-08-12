# Runbook - Deploying the redesigned timely-asp (DataRobot + Databricks)

Prerequisites
- AWS account with permissions to create IAM roles and EC2 instances.
- Databricks workspace and a personal access token (for Terraform or CI to create jobs/secret-scopes).
- DataRobot account and an API key associated with a model deployment.
- Terraform (>= 1.0) installed locally or in CI.

Quick deploy (high-level)
1. Clone the repo and checkout the branch `redesign/datarobot-databricks`.
2. Populate Terraform variables (see infra/terraform/variables.tf) and configure backend/state.
3. terraform init && terraform plan && terraform apply
4. In Databricks: create secret scopes (if not created by Terraform) and add secrets: DATAROBOT_API_KEY, DATABRICKS_TOKEN.
5. On EC2 (or local testing): create a `.env` with values from config/example.env and install requirements.
6. Start the EC2 agent as a systemd service or run via supervisor: `python3 src/agent/ec2_agent.py`.
7. Validate: trigger a small job that ingests a sample file from S3 and run inference for a small batch.

Rollback
- Destroy the Terraform-managed infra: `terraform destroy` (be careful; this will remove resources).
- Revoke and rotate any leaked secrets.

Troubleshooting
- Databricks authentication errors: verify DATABRICKS_HOST and DATABRICKS_TOKEN and that the token has appropriate scope.
- DataRobot errors: check the DATAROBOT_API_KEY and deployment ID; validate with a small sample payload.
- EC2 agent can't read S3: check the instance profile and attached IAM policy.

Contact
- Refer to the SECURITY.md for secret handling and escalation steps.