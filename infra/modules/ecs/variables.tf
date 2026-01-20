variable "cluster_name" {
  type        = string
  description = "Name of the ECS cluster"
}

variable "family" {
  type        = string
  description = "Family name for the task definition"
}

variable "cpu" {
  type        = string
  description = "CPU units for the task"
  default     = "256"
}

variable "memory" {
  type        = string
  description = "Memory for the task"
  default     = "512"
}

variable "execution_role_arn" {
  type        = string
  description = "ARN of the ECS execution role"
}

variable "image" {
  type        = string
  description = "Container image URI"
}

variable "secret_arn" {
  type        = string
  description = "ARN of the secrets manager secret"
}

variable "log_group_name" {
  type        = string
  description = "Name of the CloudWatch log group"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
}

variable "subnets" {
  type        = list(string)
  description = "List of subnet IDs for the ECS service"
}

variable "security_group_id" {
  type        = string
  description = "Security group ID for the ECS service"
}
