locals {
  dns_names = concat([{
    name  = var.domain_name
    value = "s3-website.eu-west-2.amazonaws.com"
    type  = "CNAME"
  }], var.dns_names)
}

resource "cloudflare_record" "dns_record" {
  count   = length(local.dns_names)
  zone_id = var.cloudflare_zone
  name    = local.dns_names[count.index].name
  value   = local.dns_names[count.index].value
  type    = local.dns_names[count.index].type
  ttl     = 1
  proxied = true
}