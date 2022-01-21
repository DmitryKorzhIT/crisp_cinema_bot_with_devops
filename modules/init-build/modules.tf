# ==========|  MODULES  |==========

module "cluster" {
  source = "./../cluster"
  aws_region = var.aws_region
  ecr_repository_url = var.ecr_repository_url
  app_name = var.app_name
  environment = var.environment
  image_tag = var.image_tag
  app_count = var.app_count
  server_port = var.server_port
  cidr_block_0 = var.cidr_block_0
  private_subnets_id = module.network.private_subnets_id
  lb_target_group_id = module.balancer.lb_target_group_id
  lb_listener = module.balancer.lb_listener
  vpc_id = module.network.vpc_id
}

module "network" {
  source = "./../network"
  app_name = var.app_name
  environment = var.environment
  count_value = var.count_value
}

module "balancer" {
  source = "./../balancer"
  app_name = var.app_name
  environment = var.environment
  server_port = var.server_port
  vpc_id = module.network.vpc_id
  public_subnets_id = module.network.public_subnets_id
  security_group_id = module.cluster.security_group_http_id
}