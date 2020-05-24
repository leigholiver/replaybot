resource "aws_s3_bucket" "public" {
  count         = length(var.buckets)
  bucket        = "%{if var.buckets[count.index].subdomain != ""}${var.buckets[count.index].subdomain}.%{endif}${var.domain_name}"
  force_destroy = true
  acl           = "public-read"

  # only allow access from cloudflare IP ranges
  # to prevent the aws bucket url from working
  # - helps ip restrictions work properly
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::%{if var.buckets[count.index].subdomain != ""}${var.buckets[count.index].subdomain}.%{endif}${var.domain_name}/*",
      "Condition": {
         "IpAddress": {
            "aws:SourceIp": ${jsonencode(compact(concat(split("\n", data.http.cf_ip4.body), split("\n", data.http.cf_ip6.body))))}
        }
      }
    }
  ]
}
EOF

  # s3 without react router routing rules
  dynamic "website" {
    for_each = var.buckets[count.index].use_react_router == "" ? [true] : []
    content {
      index_document = "index.html"
      error_document = "error.html"
    }
  }

  # s3 with react router routing rules
  dynamic "website" {
    for_each = var.buckets[count.index].use_react_router != "" ? [true] : []
    content {
      index_document = "index.html"
      error_document = "error.html"
      routing_rules  = <<EOF
      [{
          "Condition": {
              "HttpErrorCodeReturnedEquals": "404"
          },
          "Redirect": {
              "HostName": "%{if var.buckets[count.index].subdomain != ""}${var.buckets[count.index].subdomain}.%{endif}${var.domain_name}",
              "ReplaceKeyPrefixWith": "#!/"
          }
      }]
      EOF
    }
  }
}

# Bucket public access policy
resource "aws_s3_bucket_public_access_block" "example" {
  #count                   = length(aws_s3_bucket.public)
  count                   = length(var.buckets)
  bucket                  = aws_s3_bucket.public[count.index].id
  block_public_acls       = false
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

# Upload content
data "external" "content_hash" {
  count   = length(var.buckets)
  program = ["python3", "lambctl", "hashpath", var.buckets[count.index].content_dir]
}

resource "null_resource" "upload_to_s3_public" {
  count = length(var.buckets)
  triggers = {
    content_dir_modified = data.external.content_hash[count.index].result["result"]
  }

  provisioner "local-exec" {
    # `--delete` - Files that exist in the destination but not in the source are deleted during sync
    # todo: fix the nasty ci hacks here
    command = "aws s3 sync $([ ! -z \"$AWS_DEFAULT_REGION\" ] || echo --profile default) --acl public-read --delete ${var.buckets[count.index].content_dir} s3://${aws_s3_bucket.public[count.index].id}"
  }
}

# Utility for cloudflare ip ranges
data "http" "cf_ip4" {
  url = "https://www.cloudflare.com/ips-v4"
}

data "http" "cf_ip6" {
  url = "https://www.cloudflare.com/ips-v6"
}