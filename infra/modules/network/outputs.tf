output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.this.id
}

output "public_subnets" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "security_group_id" {
  description = "ID of the ECS security group"
  value       = aws_security_group.ecs.id
}
