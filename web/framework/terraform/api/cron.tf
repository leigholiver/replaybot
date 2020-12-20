resource "aws_cloudwatch_event_rule" "event_rule" {
  count               = length(var.cron_jobs)
  name                = "${var.identifier}_${var.cron_jobs[count.index].name}"
  description         = lookup(var.cron_jobs[count.index], "description", "")
  schedule_expression = var.cron_jobs[count.index].rate
}

resource "aws_cloudwatch_event_target" "event_target" {
  count = length(aws_cloudwatch_event_rule.event_rule)
  rule  = aws_cloudwatch_event_rule.event_rule[count.index].name
  arn   = aws_lambda_function.lambda.arn
  input = jsonencode(lookup(var.cron_jobs[count.index], "data", ""))
}

resource "aws_lambda_permission" "event_permission" {
  count         = length(aws_cloudwatch_event_rule.event_rule)
  statement_id  = "${var.cron_jobs[count.index].name}_permission"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.event_rule[count.index].arn
}
