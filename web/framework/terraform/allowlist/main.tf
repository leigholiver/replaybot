locals {
  ipv4 = var.cloudflare_on ? compact(split("\n", data.http.cloudflare_ipv4.body)) : var.allowed_ips
  ipv6 = var.cloudflare_on ? compact(split("\n", data.http.cloudflare_ipv6.body)) : []
}

data "http" "cloudflare_ipv4" {
  url = "https://www.cloudflare.com/ips-v4"
}

data "http" "cloudflare_ipv6" {
  url = "https://www.cloudflare.com/ips-v6"
}

resource "aws_wafv2_ip_set" "cf_ipv4" {
  count              = var.waf_on ? 1 : 0
  name               = "${var.identifier}_AllowlistIPv4"
  scope              = var.scope
  ip_address_version = "IPV4"
  addresses          = local.ipv4
}

resource "aws_wafv2_ip_set" "cf_ipv6" {
  count              = var.waf_on ? 1 : 0
  name               = "${var.identifier}_AllowlistIPv6"
  scope              = var.scope
  ip_address_version = "IPV6"
  addresses          = local.ipv6
}

resource "aws_wafv2_web_acl" "allowlist" {
  count = var.waf_on ? 1 : 0
  name  = "${var.identifier}_ipallow"
  scope = var.scope

  default_action {
    block {}
  }

  rule {
    name     = "${var.identifier}_ipallow_rule"
    priority = 1

    action {
      allow {}
    }

    statement {
      or_statement {
        statement {
          ip_set_reference_statement {
            arn = aws_wafv2_ip_set.cf_ipv4[count.index].arn
          }
        }
        statement {
          ip_set_reference_statement {
            arn = aws_wafv2_ip_set.cf_ipv6[count.index].arn
          }
        }
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = false
      metric_name                = "${var.identifier}_ipallow_rule_metric"
      sampled_requests_enabled   = false
    }
  }
  visibility_config {
    cloudwatch_metrics_enabled = false
    metric_name                = "${var.identifier}_ipallow_metric"
    sampled_requests_enabled   = false
  }
}
