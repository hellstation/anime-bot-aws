variable "aws_region" {
  default = "eu-north-1"
}

variable "subnets" {
  type = list(string)
}

variable "security_group_id" {
  type = string
}

variable "telegram_bot_token" {
  type        = string
  description = "Telegram bot token"
}

variable "telegram_chat_id" {
  type        = string
  description = "Telegram chat ID"
}
