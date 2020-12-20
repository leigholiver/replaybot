variable "waf_on" {
  description = "create resources? workaround for not being able to conditionally include modules. enabling waf incurs charges"
  type        = bool
  default     = true
}

variable "identifier" {
  description = "identifier for resource naming"
  type        = string
}

variable "scope" {
  description = "waf acl scope, `REGIONAL` or `CLOUDFRONT`"
  type        = string
}

variable "allowed_ips" {
  description = "allowed cidr ranges"
  type        = list(string)
  default     = []
}

variable "cloudflare_on" {
  description = "restrict access to cloudflare ip ranges - overrides allowed_ips"
  type        = bool
  default     = true
}
