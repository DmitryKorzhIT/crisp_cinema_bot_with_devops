# ==========| INITIALIZING GLOBALS VARIABLES |==========

variable aws_region {}
variable ecr_repository_url {}
variable app_name {}
variable environment {}
variable image_tag {}
variable app_count {}
variable server_port {}
variable cidr_block_0 {}


# ==========| VARIABLES FOR "CLUSTER" MODULE |==========

variable "task_definition_template" {
  description = "JSON Template file for resource task_definition"
  type        = string
  default     = "./../cluster/def.json.tpl"
}

variable "launch_type" {
  description = "AWS-managed infrastructure 'FARGATE'"
  type        = string
  default     = "FARGATE"
}

variable "network_mode" {
  description = "Network mode"
  type        = string
  default     = "awsvpc"
}

variable "fargate_cpu" {
  description = "Fargate instance CPU units to provision (1 vCPU = 1024 CPU units)"
  type        = string
  default     = "256"
}

variable "fargate_memory" {
  description = "Fargate instance memory to provision (in MiB)"
  type        = string
  default     = "512"
}

variable "ecs_task_execution_role_name" {
  description = "ECS task execution role name"
  type        = string
  default     = "TaskExecutionRole"
}

variable "ecs_task_role_name" {
  description = "ECS task role name"
  type        = string
  default     = "TaskRole"
}

variable "protocol_tcp" {
  description = "Protocol 'TCP'"
  type        = string
  default     = "tcp"
}

locals {
  container_name  = format("%s-%s-app", var.app_name, var.environment)
  app_image       = format("%s/%s-%s:%s", var.ecr_repository_url, var.app_name, var.environment, var.image_tag)
}


# ==========|  IMPORT VARIABLES FROM OTHER MODULES  |==========

variable "private_subnets_id" {
  description = "Private Subnets ID"
  type        = list(string)
  default     = null
}

variable "lb_target_group_id" {
  description = "ALB Target Group ID"
  type        = string
  default     = null
}

variable "lb_listener" {
  description = "ALB Listener"
#  type        = any
  default     = null
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
  default     = null
}