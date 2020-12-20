output "arn" {
  value = var.waf_on ? aws_wafv2_web_acl.allowlist[0].arn : null
}
