output "ecr_repository_url" {
  value = module.ecr.repository_url
}

output "ecs_cluster_name" {
  value = module.ecs.cluster_name
}

output "ecs_task_definition_arn" {
  value = module.ecs.task_definition_arn
}
