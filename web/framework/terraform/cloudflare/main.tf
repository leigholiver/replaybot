locals {
  dns_names = [
    for dns_name_key, dns_name in var.dns_names : {
      name    = dns_name.name
      value   = dns_name.value
      type    = dns_name.type
      ttl     = lookup(dns_name, "ttl", 1)
      proxied = lookup(dns_name, "proxied", var.cloudflare_on ? 1 : 0)
    }
  ]
}

resource "cloudflare_record" "dns_record" {
  count   = length(local.dns_names)
  zone_id = var.cloudflare_zone
  name    = local.dns_names[count.index].name
  value   = local.dns_names[count.index].value
  type    = local.dns_names[count.index].type
  ttl     = local.dns_names[count.index].ttl
  proxied = local.dns_names[count.index].proxied
}

resource "cloudflare_worker_route" "ip_allowlist" {
  count       = var.cloudflare_on ? length(local.dns_names) : 0
  zone_id     = var.cloudflare_zone
  pattern     = "${local.dns_names[count.index].name}/*"
  script_name = cloudflare_worker_script.ip_allowlist[0].name
}

resource "cloudflare_worker_script" "ip_allowlist" {
  count = var.cloudflare_on ? 1 : 0
  name  = "${var.identifier}_allowlist"
  content = templatefile("${path.module}/worker.js.tpl", {
    allowed_ips = var.allowed_ips
  })
}
