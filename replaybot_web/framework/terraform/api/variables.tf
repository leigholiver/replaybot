variable "project_name" {
  type = string
}

variable "name" {
  type = string
}

variable "region" {
  type = string
}

variable "env_vars" {
  type    = map(string)
  default = {}
}

# cron(0 20 * * ? *) or rate(5 minutes)
variable "cron_jobs" {
  type    = list(map(string))
  default = []
}

variable "allowed_ips" {
  type    = list(string)
  default = []
}

variable "source_dir" {
  type    = string
  default = "./.build"
}

variable "lambda_zip" {
  type    = string
  default = "./.build/api_lambda.zip"
}

variable "api_path" {
  type    = string
  default = "api"
}

variable "log_retention_days" {
  type    = number
  default = 1
}

# it looks tempting to decrease lambda_memory becuase cloudwatch reckons you 
# only use max 80mb, but it actually starts to time out if you drop it?
variable "lambda_memory" {
  type    = number
  default = 256 # in mb
}

variable "lambda_timeout" {
  type    = number
  default = 8 # in seconds
}