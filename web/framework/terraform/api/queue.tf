resource "aws_lambda_event_source_mapping" "job_queue_lambda_mapping" {
  event_source_arn = aws_sqs_queue.job_queue.arn
  function_name    = aws_lambda_function.lambda.arn
}

resource "aws_sqs_queue" "job_queue" {
  name                       = "${var.identifier}_job_queue"
  visibility_timeout_seconds = 3600
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.deadletter_queue.arn
    maxReceiveCount     = 5
  })
}

resource "aws_sqs_queue" "deadletter_queue" {
  name                       = "${var.identifier}_deadletter_queue"
  visibility_timeout_seconds = 3600
}

resource "aws_sqs_queue" "test_queue" {
  name                       = "${var.identifier}_test_queue"
  visibility_timeout_seconds = 3600
}

resource "aws_iam_policy" "queue_policy" {
  name        = "${var.identifier}_queue"
  path        = "/"
  description = "IAM policy for sqs queue from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "sqs:ListQueues",
        "sqs:SendMessage",
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes",
        "sqs:ChangeMessageVisibility",
        "sqs:GetQueueUrl"
      ],
      "Resource": "${aws_sqs_queue.deadletter_queue.arn}",
      "Effect": "Allow"
    },
    {
      "Action": [
        "sqs:ListQueues",
        "sqs:SendMessage",
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes",
        "sqs:ChangeMessageVisibility",
        "sqs:GetQueueUrl"
      ],
      "Resource": "${aws_sqs_queue.test_queue.arn}",
      "Effect": "Allow"
    },
    {
      "Action": [
        "sqs:ListQueues",
        "sqs:SendMessage",
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes",
        "sqs:ChangeMessageVisibility",
        "sqs:GetQueueUrl"
      ],
      "Resource": "${aws_sqs_queue.job_queue.arn}",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "lambda_queue" {
  name       = "${var.identifier}_queue_attachment"
  roles      = [aws_iam_role.role.name]
  policy_arn = aws_iam_policy.queue_policy.arn
}
