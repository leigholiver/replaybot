variable "identifier" {
  description = "prefix for resource naming"
  type        = string
}

variable "lambda_zip" {
  description = "location to build the lambda zip package to"
  type        = string
}

variable "zip_hash" {
  description = "hash of the zip file. if ommited will be calculated but may run into dependency issues"
  type        = string
  default     = null
}

variable "custom_domain_name" {
  description = "custom domain name to use for the api"
  type        = string
  default     = null
}

variable "api_path" {
  description = "api gateway stage, https://{api_domain}/{api_path}"
  type        = string
  default     = "api"
}

variable "cert_arn" {
  description = "arn of the acm certificate, required if using custom domain name"
  type        = string
  default     = null
}

variable "waf_arn" {
  description = "arn of aws wafv2 to associate - enabling this incurs a charge"
  default     = null
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

variable "env_vars" {
  description = "lambda environment variables"
  type        = map(string)
  default     = {}
}

variable "cron_jobs" {
  description = "list of scheduled executions. rate: any string understood by cloudwatch, cron(0 20 * * ? *) or rate(5 minutes)"
  type = list(object({
    name = string
    rate = string
    data = any
  }))
  default = []
}

variable "log_retention_days" {
  description = "number of days to keep cloudwatch logs for"
  type        = string
  default     = 1
}

variable "lambda_memory" {
  description = "memory to use for the lambda in mb"
  type        = string
  default     = 256 # in mb
}

variable "lambda_timeout" {
  description = "lambda request timeout in seconds"
  type        = string
  default     = 8 # in seconds
}
