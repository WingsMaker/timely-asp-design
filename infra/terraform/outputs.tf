# Example outputs
output "ec2_agent_instance_id" {
  value = aws_instance.agent.id
}

output "databricks_secret_scope_name" {
  value = databricks_secret_scope.timely_asp.name
}
