# lamb-tf
terraform modules for [lamb](https://github.com/leigholiver/lamb)

see readme.md in module directories for usage

* `allowlist` wafv2 acl to allow access for specific ip ranges
    * (warning: incurs a charge compared to the rest of the modules - $7/mo)
* `api` lambda api gateway with custom domain name support, dynamodb, sqs
* `cert` acm certificate validated by cloudflare dns challenge
* `cloudflare` dns names and allowlist worker routes
* `gather` utility module to package pip deps and source code into a zip file
* `hashpath` utility module for hashing file or directory paths
* `lamb` main lamb module, ties together the other modules
* `public` s3 bucket with cloudfront
