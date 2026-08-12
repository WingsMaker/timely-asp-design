variable "aws_region" {
  description = "AWS region to deploy resources in"
  type        = string
  default     = "us-west-2"
}

variable "ec2_instance_type" {
  description = "EC2 instance type for the agent"
  type        = string
  default     = "t3.small"
}

variable "s3_ingest_bucket" {
  description = "S3 bucket used for raw input"
  type        = string
}

variable "databricks_host" {
  description = "Databricks workspace host (https://<instance>)"
  type        = string
  default     = ""
}

variable "databricks_token" {
  description = "Databricks PAT token"
  type        = string
  default     = ""
}
