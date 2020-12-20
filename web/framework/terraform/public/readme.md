# public
module to create one or more s3 bucket websites with cloudfront

#### variables
* `buckets` list of bucket objects to create
  * `content_dir` the path to the bucket contents
  * `domain_name` the subdomain to use
  * `use_react_router` [optional] enable react router redirects to #! on 404 (default: false)
* `cert_arn` the arn of the acm certificate to associate with cloudfront
* `waf_arn` [optional] the arn of the allowlist to associate with cloudfront (enabling will incur charges)

#### outputs
* `endpoints` a list of bucket domain names and their associated cloudfront endpoints
