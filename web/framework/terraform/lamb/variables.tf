variable "project_name" {
  description = "name of the project"
  type        = string
}

variable "env_name" {
  description = "name of the environment"
  type        = string
}

variable "domain_name" {
  description = "domain name to deploy to"
  type        = string
}

variable "cloudflare_zone" {
  description = "cloudflare zone id for the domain"
  type        = string
}

variable "lamb_config" {
  description = "lamb optional configuration - see lamb_configuration_defaults variable"
  default     = {}
}

variable "lamb_config_defaults" {
  type = object({
    api_subdomain   = string
    api_domain_name = string
    allowed_ips     = list(string)
    cloudflare_on   = bool
    waf_on          = bool
    dns_names = list(object({
      name    = string
      value   = string
      type    = string
      proxied = any
      ttl     = any
    }))
  })
  default = {
    api_subdomain   = "api"
    api_domain_name = ""
    allowed_ips     = []
    cloudflare_on   = true
    waf_on          = false
    dns_names       = []
  }
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

variable "build_config" {
  description = "build optional configuration - see build_config_defaults variable"
  default     = {}
}

variable "build_config_defaults" {
  type = object({
    source_dir   = string
    support_dir  = string
    requirements = string
    build_dir    = string
    zip_path     = string
  })
  default = {
    source_dir   = "./api"
    support_dir  = "./framework/lamb"
    requirements = "./api/packages.txt"
    build_dir    = "./.build/build"
    zip_path     = "./.build/api_lambda.zip"
  }
}

variable "api_config" {
  description = "api optional configuration - see api_config_defaults variable"
  default     = {}
}

variable "api_config_defaults" {
  type = object({
    env_vars           = map(string)
    cron_jobs          = list(map(string))
    api_path           = string
    log_retention_days = number
    lambda_memory      = number
    lambda_timeout     = number
  })

  default = {
    env_vars           = {}
    cron_jobs          = []
    api_path           = "api"
    log_retention_days = 1
    lambda_memory      = 256
    lambda_timeout     = 8
  }
}

variable "tables" {
  description = "map of dynamodb model tables to create"
  type = list(object({
    expires  = string
    indexes  = list(string)
    name     = string
    sort_key = string
  }))
}
