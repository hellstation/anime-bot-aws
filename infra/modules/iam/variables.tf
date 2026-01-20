variable "role_name" {
  type        = string
  description = "Name of the ECS execution role"
}

variable "secret_arn" {
  type        = string
  description = "ARN of the secrets manager secret"
}
