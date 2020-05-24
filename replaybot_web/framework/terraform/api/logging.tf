resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/lambda/${var.project_name}_${var.name}_lambda"
  retention_in_days = var.log_retention_days
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "${var.project_name}_${var.name}_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_logs" {
  name       = "${var.project_name}_${var.name}_logs_attachment"
  roles      = [aws_iam_role.role.name]
  policy_arn = aws_iam_policy.lambda_logging.arn
}