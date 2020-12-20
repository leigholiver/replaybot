terraform {
  backend "s3" {}
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

provider "aws" {
  alias  = "useast"
  region = "us-east-1"
}

provider "cloudflare" {
  email      = var.cloudflare_email
  api_key    = var.cloudflare_apikey
  account_id = var.cloudflare_account_id
}

locals {
  lamb_config  = merge(var.lamb_config_defaults, var.lamb_config)
  build_config = merge(var.build_config_defaults, var.build_config)
  api_config   = merge(var.api_config_defaults, var.api_config)
}

module "lamb" {
  source = "./framework/terraform/lamb"
  providers = {
    aws        = aws
    aws.useast = aws.useast
  }
  project_name    = var.project_name
  env_name        = var.env_name
  domain_name     = var.domain_name
  cloudflare_zone = var.cloudflare_zone
  lamb_config     = local.lamb_config
  build_config    = local.build_config
  api_config      = local.api_config
  tables          = var.tables
  buckets         = var.buckets
}
