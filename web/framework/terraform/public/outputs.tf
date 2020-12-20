output "endpoints" {
  value = [
    for pair in setproduct(local.buckets, aws_cloudfront_distribution.cf_distro) : {
      domain_name = pair[0].domain_name
      endpoint    = pair[1].domain_name
    }
  ]
}
