#"Resource": "execute-api:/*/*/*"
resource "aws_api_gateway_rest_api" "api" {
  name   = "${var.project_name}_${var.name}_api_endpoints"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:*:*:*"
      %{if length(var.allowed_ips) > 0}
        ,
        "Condition": {
          "IpAddress": {
            "aws:SourceIp": [%{for index, ip in var.allowed_ips}
              "${ip}"%{if index < length(var.allowed_ips) - 1},%{endif}
            %{endfor}]
          }
        }
      %{endif}
    }
  ]
}
EOF
}

resource "aws_api_gateway_resource" "endpoint" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.endpoint.id
  http_method   = "ANY"
  authorization = "NONE"
  request_parameters = {
    "method.request.path.proxy" = true
  }
}

resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.endpoint.id
  http_method             = aws_api_gateway_method.method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda.invoke_arn
  request_parameters = {
    "integration.request.path.proxy" = "method.request.path.proxy"
  }
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on  = [aws_api_gateway_integration.integration]
  rest_api_id = aws_api_gateway_rest_api.api.id
  stage_name  = var.api_path

  # hack to redeploy whenever the env file changes
  # makes sure that the allowed IPs list updates
  variables = {
    "release" = sha1(file("env.auto.tfvars.json"))
  }
}
