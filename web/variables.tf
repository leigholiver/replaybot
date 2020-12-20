variable "aws_profile" {
  description = "name of the aws profile to use"
  type        = string
  default     = "default"
}

variable "aws_region" {
  description = "aws region to create the resources in"
  type        = string
  default     = "eu-west-2"
}

variable "cloudflare_account_id" {
  description = "cloudflare account id"
  type        = string
}

variable "cloudflare_email" {
  description = "cloudflare account email adddress"
  type        = string
}

variable "cloudflare_apikey" {
  description = "cloudflare api key"
  type        = string
}
