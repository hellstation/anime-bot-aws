resource "aws_cloudwatch_event_rule" "schedule" {
  name                = var.rule_name
  schedule_expression = var.schedule_expression
}
