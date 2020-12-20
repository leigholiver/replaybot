# allowlist
module to provide an `aws_wafv2_web_acl` for either `var.allowed_ips` or cloudflare ip ranges if `cloudflare_on` is `true`. when `cloudflare_on` is true, access restrictions can be handled by the lamb cloudflare module

warning if youre trying to do things cheap like me: wafv2 acls incur a $5 monthly charge, plus $2 in ipset rules (ipv4/ipv6)

#### variables
* `identifier` identifier for naming resources
* `waf_on` create resources? workaround for not being able to conditionally include modules. enabling waf incurs charges (default: `true`)
* `allowed_ips` cidr ranges to allow access to
* `scope` the scope of the `aws_wafv2_web_acl`, `"REGIONAL"` or `"CLOUDFRONT"`. for lamb, regional is for lambda and cloudfront is for s3 buckets
* `cloudflare_on` if `true`, will restrict access to cloudflare ip ranges, so that cloudflare workers in the `cloudflare` module can restrict access

#### outputs
* `arn` the arn of the `aws_wafv2_web_acl`, or `null` if `waf_on` is `false`
