provider "aws" {
  alias = "useast"
}

locals {
  identifier      = "${var.project_name}_${var.env_name}"
  lamb_config     = merge(var.lamb_config_defaults, var.lamb_config)
  build_config    = merge(var.build_config_defaults, var.build_config)
  api_config      = merge(var.api_config_defaults, var.api_config)
  api_domain_name = local.lamb_config.api_domain_name == "" ? "${local.lamb_config.api_subdomain}.${var.domain_name}" : local.lamb_config.api_domain_name
  cloudflare_zone = local.lamb_config.cloudflare_zone != "" ? local.lamb_config.cloudflare_zone : var.cloudflare_zone
  dns_names = concat(
    local.lamb_config.dns_names,
    [for endpoint_key, endpoint in module.public.endpoints : {
      name  = endpoint.domain_name
      value = endpoint.endpoint
      type  = "CNAME"
    }],
    [{
      name  = local.api_domain_name
      value = module.api.endpoint
      type  = "CNAME"
    }]
  )
}

# dns names, allowlist worker
module "cloudflare" {
  source          = "../cloudflare"
  cloudflare_zone = local.cloudflare_zone
  identifier      = local.identifier
  dns_names       = local.dns_names
  allowed_ips     = local.lamb_config.allowed_ips
  cloudflare_on   = local.lamb_config.cloudflare_on
}

# package the dependencies + src code
module "gather" {
  source  = "../gather"
  src_dir = local.build_config.source_dir
  additional_dirs = [{
    dir      = local.build_config.support_dir
    basepath = local.build_config.support_dir
  }]
  requirements = local.build_config.requirements
  build_dir    = local.build_config.build_dir
  zip_path     = local.build_config.zip_path
}

# lambda, api gateway
module "api" {
  source             = "../api"
  identifier         = local.identifier
  custom_domain_name = local.api_domain_name
  cert_arn           = module.api_cert.arn
  waf_arn            = module.api_waf.arn
  tables             = var.tables
  env_vars = merge(local.api_config.env_vars, {
    "PROJECT_NAME" = var.project_name
    "LAMB_ENV"     = var.env_name
  })
  cron_jobs = concat([{
    name = "${local.identifier}_wool"
    rate = "rate(10 minutes)"
    data = jsonencode(["wool"])
  }], local.api_config.cron_jobs)
  lambda_zip         = module.gather.zip_path
  zip_hash           = module.gather.base64sha256
  api_path           = local.api_config.api_path
  log_retention_days = local.api_config.log_retention_days
  lambda_memory      = local.api_config.lambda_memory
  lambda_timeout     = local.api_config.lambda_timeout
}

module "api_cert" {
  source          = "../cert"
  cloudflare_zone = local.cloudflare_zone
  domain_name     = local.api_domain_name
}

module "api_waf" {
  source        = "../allowlist"
  identifier    = local.identifier
  waf_on        = local.lamb_config.waf_on
  cloudflare_on = local.lamb_config.cloudflare_on
  allowed_ips   = local.lamb_config.allowed_ips
  scope         = "REGIONAL"
}

# s3 buckets with cloudfront
module "public" {
  source   = "../public"
  buckets  = var.buckets
  cert_arn = module.public_cert.arn
  waf_arn  = module.public_waf.arn
}

module "public_cert" {
  source = "../cert"
  providers = {
    aws = aws.useast
  }
  cloudflare_zone   = local.cloudflare_zone
  domain_name       = var.domain_name
  alternative_names = [for bucket_key, bucket in var.buckets : bucket.domain_name]
}

module "public_waf" {
  source = "../allowlist"
  providers = {
    aws = aws.useast
  }
  identifier    = local.identifier
  waf_on        = local.lamb_config.waf_on
  cloudflare_on = local.lamb_config.cloudflare_on
  allowed_ips   = local.lamb_config.allowed_ips
  scope         = "CLOUDFRONT"
}
