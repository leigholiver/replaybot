variable "cloudflare_zone" {
  type = string
}

variable "project_name" {
  type = string
}

variable "name" {
  type = string
}

# domain name to use for the public module s3 bucket
variable "domain_name" {
  type = string
}

variable "allowed_ips" {
  type    = list(string)
  default = []
}

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