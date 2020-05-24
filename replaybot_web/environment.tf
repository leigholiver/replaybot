# name of the project
variable "project_name" {
  type = string
}

# name of the environment
variable "env_name" {
  type = string
}

# domain name to use
# eg example.com
variable "domain_name" {
  type = string
}

# s3 bucket websites
# {
#    "content_dir"      = "./testbucket", # the directory path with the bucket contents
#    "subdomain"        = "testing",      # [optional] the subdomain to use, default main domain
#    "use_react_router" = "true"            # [optional] enable react router compatibility, default false
# }
variable "buckets" {
  type    = list(map(string))
  default = []
}

# directory of the gathered api lambda source code
variable "source_dir" {
  type    = string
  default = "./.build"
}

# domain name for the api eg api.example.com
variable "api_domain" {
  type    = string
  default = ""
}

###
# api variables
###
# environment variables for the lambda 
# { "key" = "value" }
variable "env_vars" {
  type    = map(string)
  default = {}
}

# allowed ip addresses or cidr blocks
# if empty, there are no restrictions
# [ "127.0.0.1", "192.168.0.2/32" ]
variable "allowed_ips" {
  type    = list(string)
  default = []
}

# list of lambctl cron jobs
# rate can be any string understood by cloudwatch, cron(0 20 * * ? *) or rate(5 minutes)
# data should be a list of arguments for lambctl, ie `lambctl tests router` would become ["tests", "router"]
# {
#   name = "wool"
#   rate = "rate(10 minutes)"
#   data = jsonencode(["wool"])
# }
variable "cron_jobs" {
  type    = list(map(string))
  default = []
}

# api gateway stage, https://{api_domain}/{api_path}
variable "api_path" {
  type    = string
  default = "api"
}

# number of days to keep cloudwatch logs for
variable "log_retention_days" {
  type    = string
  default = 1
}

# path to temporary build zip
variable "lambda_zip" {
  type    = string
  default = "./.build/api_lambda.zip"
}

# memory to use for the lambda in mb
variable "lambda_memory" {
  type    = string
  default = 256 # in mb  
}

# lambda request timeout in seconds
variable "lambda_timeout" {
  type    = string
  default = 8 # in seconds  
}

###
# dynamodb table variables
###
# list of dynamodb tables to create
variable tables {
  # [{
  #     name     = "" # the name of the table
  #     expires  = "" # expiry timestamp, if this is "" then ttl is disabled
  #     sort_key = "" # index to use as a sort key
  #     indexes  = [] # any extra indexes to create
  # }]
}

###
# cloudflare variables
###
# list of additional dns names to create
# required: { name = domain.com, value = s3-bucket-url.com, type = CNAME }
# creates: cloudflare dns name
variable "dns_names" {
  type    = list(map(string))
  default = []
}

# required: { from = domain.com, to = www.domain.com }
# creates: cloudflare dns name for "from", CNAME to "to"
# creates: worker rule on path "from", redirecting requests to "to", forcing https
variable "www_redirects" {
  type    = list(map(string))
  default = []
}

# required: { from = domain.com/api, to = lambda-endpoint.com/api }
# creates: worker rule on path "from", redirecting requests to "to", forcing https
# and adding an access-control-allow-origin header for cors compatibility
variable "api_redirects" {
  type    = list(map(string))
  default = []
}