# Terraform skeleton for timely-asp redesign

terraform {
  required_version = ">= 1.0"
}

# Providers: fill provider configurations and credentials before running
provider "aws" {
  region = var.aws_region
}

# databricks provider requires host and token. Set via environment or provider block.
provider "databricks" {
  # host  = var.databricks_host
  # token = var.databricks_token
}

# NOTE: This file is a skeleton. Use the other .tf files (iam.tf, ec2.tf, databricks.tf) to define resources.
