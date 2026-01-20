variable "rule_name" {
  type        = string
  description = "Name of the EventBridge rule"
}

variable "schedule_expression" {
  type        = string
  description = "Schedule expression for the rule"
  default     = "rate(1 hour)"
}
