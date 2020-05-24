locals {
  jobs = concat([{
    name = "${var.project_name}_${var.name}_wool"
    rate = "rate(10 minutes)"
    data = jsonencode(["wool"])
  }], var.cron_jobs)
}

resource "aws_cloudwatch_event_rule" "event_rule" {
  count               = length(local.jobs)
  name                = "${var.project_name}_${var.name}_${local.jobs[count.index].name}"
  description         = lookup(local.jobs[count.index], "description", "")
  schedule_expression = local.jobs[count.index].rate
}

resource "aws_cloudwatch_event_target" "event_target" {
  count = length(aws_cloudwatch_event_rule.event_rule)
  rule  = aws_cloudwatch_event_rule.event_rule[count.index].name
  arn   = aws_lambda_function.lambda.arn
  input = jsonencode(lookup(local.jobs[count.index], "data", ""))
}

resource "aws_lambda_permission" "event_permission" {
  count         = length(aws_cloudwatch_event_rule.event_rule)
  statement_id  = "${local.jobs[count.index].name}_permission"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.event_rule[count.index].arn
}