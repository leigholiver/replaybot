# lamb
main terraform module for [lamb](https://github.com/leigholiver/lamb)

lamb makes use of multiple aws regions so you must provide a `useast` aliased aws provider as well as your region provider
```
module "lamb" {
  source = "../lamb"
  providers = {
    aws        = aws
    aws.useast = aws.useast
  }
  ...
}
```

* `project_name` name of the project
* `env_name` name of the environment
* `domain_name` primary domain name
* `cloudflare_zone` cloudflare zone id for the primary domain name
* `buckets` list of buckets to create, see `public/readme.md`
* `api_config` additional parameters to pass to the `api` module, see `api/readme.md`
* `tables` tables variable to pass to the `api` module, see `api/readme.md`
* `lamb_config` configuration object
    * `api_subdomain` subdomain to use for the api (eg `api.${domain_name}`) (default `api`)
    * `api_domain_name` full domain name to use for the api - overrides `api_subdomain`
    * `cloudflare_on` cloudflare proxying enabled. if you are using `off`/`flexible` ssl mode on cloudflare, you will need to set this to false (default: `true`)
    * `allowed_ips` ips/cidr ragnes allowed to access the resources (default: `[]`, no restrictions)
    * `waf_on` create waf rules for ip restrictions (default: `false`) **will incur ~$12/mo charges**
    * `dns_names` a list of additional dns names to create. attributes match the `cloudflare_record` terraform resource (default: `[]`)
* `build_config` configuration object
    * `source_dir` path to the lambda source code (default: `./api`)
    * `support_dir` path to the lamb framework support directory
    * `requirements` path to the requirements.txt (default: `api/requirements.txt`)
    * `build_dir` path to build code/pip deps to (default: `./.build/build`)
    * `zip_path` output path for the lambda zip package (default: `./.build/api_lambda.zip`)
