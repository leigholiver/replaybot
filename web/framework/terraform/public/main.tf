resource "aws_s3_bucket" "public" {
  count         = length(local.buckets)
  bucket        = local.buckets[count.index].domain_name
  force_destroy = true
  acl           = "public-read"

  # only allow access from cloudfront IP ranges to prevent the
  # bucket url from working - helps ip allowlist work properly
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::${local.buckets[count.index].domain_name}/*",
      "Condition": {
         "IpAddress": {
            "aws:SourceIp": ${jsonencode(data.aws_ip_ranges.cloudfront_ranges.cidr_blocks)}
        }
      }
    }
  ]
}
EOF

  # s3 without react router routing rules
  dynamic "website" {
    for_each = local.buckets[count.index].use_react_router == "" ? [true] : []
    content {
      index_document = "index.html"
      error_document = "error.html"
    }
  }

  # s3 with react router routing rules
  dynamic "website" {
    for_each = local.buckets[count.index].use_react_router != "" ? [true] : []
    content {
      index_document = "index.html"
      error_document = "error.html"
      routing_rules  = <<EOF
      [{
          "Condition": {
              "HttpErrorCodeReturnedEquals": "404"
          },
          "Redirect": {
              "HostName": "${local.buckets[count.index].domain_name}",
              "ReplaceKeyPrefixWith": "#!/"
          }
      }]
      EOF
    }
  }
}

# Bucket public access policy
resource "aws_s3_bucket_public_access_block" "example" {
  count                   = length(local.buckets)
  bucket                  = aws_s3_bucket.public[count.index].id
  block_public_acls       = false
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

# Upload content
module "hashes" {
  source = "../hashpath"
  paths  = [for bucket_key, bucket in local.buckets : bucket.content_dir]
}

resource "null_resource" "upload_to_s3_public" {
  count = length(local.buckets)
  triggers = {
    content_dir_modified = module.hashes.hashes[count.index]
  }

  provisioner "local-exec" {
    # `--delete` - Files that exist in the destination but not in the source are deleted during sync
    # todo: fix the nasty ci hacks here
    command = "aws s3 sync $([ ! -z \"$AWS_DEFAULT_REGION\" ] || echo --profile default) --acl public-read --delete ${local.buckets[count.index].content_dir} s3://${aws_s3_bucket.public[count.index].id}"
  }
}

data "aws_ip_ranges" "cloudfront_ranges" {
  services = ["cloudfront"]
}
