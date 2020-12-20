output "endpoint" {
  value = var.custom_domain_name == null ? aws_api_gateway_deployment.deployment.invoke_url : try(aws_api_gateway_domain_name.domain_name[0].regional_domain_name, null)
}
