locals {
  env_vars = merge({
    "PROJECT_NAME" = var.project_name
    "LAMB_ENV"     = var.name
  }, var.env_vars)
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = var.lambda_zip
}

resource "aws_lambda_function" "lambda" {
  filename         = var.lambda_zip
  function_name    = "${var.project_name}_${var.name}_lambda"
  role             = aws_iam_role.role.arn
  handler          = "lambda_handler.lambda_handler"
  runtime          = "python3.7"
  source_code_hash = filebase64sha256(var.lambda_zip)
  memory_size      = var.lambda_memory
  timeout          = var.lambda_timeout
  environment {
    variables = local.env_vars
  }
}