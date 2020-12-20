resource "aws_cloudfront_distribution" "cf_distro" {
  count      = length(local.buckets)
  enabled    = true
  aliases    = [local.buckets[count.index].domain_name]
  web_acl_id = var.waf_arn

  origin {
    domain_name = aws_s3_bucket.public[count.index].website_endpoint
    origin_id   = local.buckets[count.index].origin_id
    custom_origin_config {
      http_port              = "80"
      https_port             = "443"
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id       = local.buckets[count.index].origin_id
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = true
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = false
    acm_certificate_arn            = var.cert_arn
    ssl_support_method             = "sni-only"
  }
}
