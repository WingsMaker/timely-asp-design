# Databricks resources (skeleton)
# Create a secret scope and a placeholder job. Expand according to your workspace & governance.

resource "databricks_secret_scope" "timely_asp" {
  name = "timely-asp-scope"
  # backend_type = "DATABRICKS" # or "AWS" for external
}

# Example: databricks job that runs a notebook or python wheel to perform ingestion/inference
resource "databricks_job" "ingest_job" {
  name = "timely-asp-ingest"
  # existing_cluster_id = var.databricks_cluster_id
  # notebook_task { notebook_path = "/Repos/.../ingest" }
}
