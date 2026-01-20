module "network" {
  source = "./modules/network"

  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
}

module "secrets" {
  source = "./modules/secrets"

  telegram_bot_token = var.telegram_bot_token
  telegram_chat_id   = var.telegram_chat_id
}

module "ecr" {
  source = "./modules/ecr"

  repository_name = "anime-notifier"
}

module "logs" {
  source = "./modules/logs"

  log_group_name = "/ecs/anime-notifier"
}

module "iam" {
  source = "./modules/iam"

  role_name   = "ecsExecutionRole"
  secret_arn  = module.secrets.secret_arn
}

module "ecs" {
  source = "./modules/ecs"

  cluster_name       = "anime-cluster"
  family             = "anime-notifier"
  execution_role_arn = module.iam.ecs_execution_role_arn
  image              = "${module.ecr.repository_url}:latest"
  secret_arn         = module.secrets.secret_arn
  log_group_name     = module.logs.log_group_name
  aws_region         = var.aws_region
  subnets            = module.network.public_subnets
  security_group_id  = module.network.security_group_id
}
