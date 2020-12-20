variable "cloudflare_zone" {
  description = "cloudflare zone id for the dns names"
  type        = string
}

variable "domain_name" {
  description = "primary domain name"
  type        = string
}

variable "alternative_names" {
  description = "alertnative domain names"
  type        = list(string)
  default     = []
}
