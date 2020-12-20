# api
aws lambda + api gateway api using a custom domain name alias

#### variables
* `identifier` used to name resources
* `source_dir` directory containing the lambda source code
* `lambda_zip` path to generate the packaged lambda zip
* `custom_domain_name` [optional] custom domain name alias to use for the api
* `api_path` api gateway stage name, `https://domain/${api_path}` (default: `api`)
* `cert_arn` [required if using custom domain name] arn to validated acm certificate for the custom domain name
* `waf_arn` [optional] wafv2 to associate with the api (**incurs a charge**)
* `tables` [optional] list of dynamodb tables to create
* `env_vars` map of environment variables for the lambda (default: `{}`)
* `cron_jobs` list of scheduled lambda executions (default: `[]`)
* `log_retention_days` number of days to keep cloudwatch logs (default: `1`)
* `lambda_memory` memory in mb (default: `256`)
* `lambda_timeout` timeout in s (default: `8`)

#### outputs
* `endpoint` the dns name for the api
