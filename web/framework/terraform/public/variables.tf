locals {
  buckets = [
    for bucket_key, bucket in var.buckets : {
      content_dir      = bucket.content_dir
      domain_name      = bucket.domain_name
      use_react_router = bucket.use_react_router == true ? true : false
      origin_id        = "CloudFront-${bucket.domain_name}"
    }
  ]
}

variable "buckets" {
  description = "list of buckets to create"
  type = list(object({
    content_dir      = string
    domain_name      = string
    use_react_router = any
  }))
  default = []
}

variable "cert_arn" {
  description = "arn of the validated acm certificate covering the domain names"
  type        = string
}

variable "waf_arn" {
  description = "arn of aws wafv2 to associate - enabling this incurs a charge"
  default     = null
}
