output "endpoint" {
  # value = "https://${aws_api_gateway_rest_api.api.id}.execute-api.${var.region}.amazonaws.com/${var.api_path}"
  value = aws_api_gateway_deployment.deployment.invoke_url
}

# used by the db module to allow the lambda access to the tables
output "role" {
  value = aws_iam_role.role
}

output "path" {
  value = var.api_path
}