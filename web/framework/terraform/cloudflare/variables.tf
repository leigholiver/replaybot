variable "cloudflare_zone" {
  type = string
}

variable "identifier" {
  type = string
}

# required: { name = domain.com, value = s3-bucket-url.com, type = CNAME }
# creates: cloudflare dns name
variable "dns_names" {
  type    = list(map(string))
  default = []
}

# enables the "proxied" mode on the api/bucket dns records
# if ssl is set to "off" or "flexible" in cloudflare, you 
# will need to set this to false
variable "cloudflare_on" {
  type    = bool
  default = true
}

# list of ip addresses or cidr ranges to restrict access to via cloudflare worker
variable "allowed_ips" {
  type    = list(string)
  default = []
}