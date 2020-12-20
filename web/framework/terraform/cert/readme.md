# cert
module to provide an acm certificate validated by cloudflare dns challenge

if you need to create a cert in another region (eg, for cloudfront), pass through an aliased provider:
```
provider "aws" {
  alias  = "useast"
  region = "us-east-1"
}

module "useast_cert" {
  source = "../cert"
  providers = {
    aws        = aws.useast
  }
  ...
}
```

#### variables
* `cloudflare_zone` the cloudflare zone_id for the domain name
* `domain_name` the primary domain name for the certificate
* `alternative_names` any subject alternative names to include

#### outputs
* `arn` the arn of the validated acm certificate
