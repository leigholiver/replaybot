# cloudflare
module to provide dns and access restriction worker scripts
note: setting `allowed_ips` has no effect if `cloudflare_on` is set to false.

#### variables
* `cloudflare_zone` zone id of the domain names
* `dns_names`  list dns name objects to create, values should
    * `name`
    * `type`
    * `value`
    * `ttl` [optional] (default `1` (auto in cloudflare))
    * `proxied` [optional] (defaults to `cloudflare_on`)
* `cloudflare_on` if `true`, will enable cloudflare proxying
* `identifier` identifier for labelling worker script
* `allowed_ips` list of ip addresses to restrict access to
