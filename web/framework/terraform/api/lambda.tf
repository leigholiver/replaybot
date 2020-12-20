resource "aws_lambda_function" "lambda" {
  filename         = var.lambda_zip
  function_name    = "${var.identifier}_lambda"
  role             = aws_iam_role.role.arn
  handler          = "lambda_handler.lambda_handler"
  runtime          = "python3.8"
  source_code_hash = var.zip_hash != null ? var.zip_hash : try(filebase64sha256(var.lambda_zip), "")
  memory_size      = var.lambda_memory
  timeout          = var.lambda_timeout
  environment {
    variables = var.env_vars
  }
}
