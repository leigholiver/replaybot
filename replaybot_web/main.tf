# name of aws cli profile to use
variable "aws_profile" {
  type    = string
  default = "default"
}

variable "aws_region" {
  type    = string
  default = "eu-west-2"
}

# these should be in a secrets.env file in TF_VAR_ environment variables
variable "cloudflare_email" {}
variable "cloudflare_apikey" {}
variable "cloudflare_account_id" {}
variable "cloudflare_zone" {}

terraform {
  backend "s3" {}
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

provider "cloudflare" {
  email      = var.cloudflare_email
  api_key    = var.cloudflare_apikey
  account_id = var.cloudflare_account_id
}

module "api" {
  source             = "./framework/terraform/api"
  project_name       = var.project_name
  name               = var.env_name
  region             = var.aws_region
  env_vars           = var.env_vars
  cron_jobs          = var.cron_jobs
  allowed_ips        = var.allowed_ips
  api_path           = var.api_path
  log_retention_days = var.log_retention_days
  source_dir         = var.source_dir
  lambda_zip         = var.lambda_zip
  lambda_memory      = var.lambda_memory
  lambda_timeout     = var.lambda_timeout
}

module "cloudflare" {
  source          = "./framework/terraform/cloudflare"
  project_name    = var.project_name
  cloudflare_zone = var.cloudflare_zone
  name            = var.env_name
  domain_name     = var.domain_name
  dns_names       = var.dns_names
  www_redirects   = var.www_redirects
  api_redirects = concat(var.api_redirects, [{
    from = "${var.api_domain != "" ? var.api_domain : var.domain_name}/${module.api.path}"
    to   = module.api.endpoint
  }])
  allowed_ips = var.allowed_ips
}

module "public" {
  source      = "./framework/terraform/public"
  aws_profile = var.aws_profile
  domain_name = var.domain_name
  buckets     = var.buckets
}

module "db" {
  source       = "./framework/terraform/db"
  project_name = var.project_name
  name         = var.env_name
  role         = module.api.role
  tables       = var.tables
}