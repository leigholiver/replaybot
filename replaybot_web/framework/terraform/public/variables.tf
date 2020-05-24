
variable "aws_profile" {
  type    = string
  default = "default"
}

# domain name, used as bucket name
variable "domain_name" {
  type = string
}

# path to content to put in the bucket
variable "buckets" {
  type = list(map(string))
}