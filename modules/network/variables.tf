# ==========| INITIALIZING GLOBAL VARIABLES |==========

variable app_name {}
variable environment {}
variable count_value {}


# ==========| VARIABLES FOR "NETWORK" MODULE |==========

variable "vpc" {
  description = "Values for VPC"
  type = object({
    cidr_block           = string
    instance_tenancy     = string
    enable_dns_hostnames = bool
  })
  default = {
    cidr_block           = "10.0.0.0/16"
    instance_tenancy     = "default"
    enable_dns_hostnames = true
  }
}

variable "public_subnet" {
  description = "Values for Public Subnets"
  type = object({
    cidr_block        = list(string)
    availability_zone = list(string)
  })
  default = {
    cidr_block        = ["10.0.10.0/24", "10.0.20.0/24"]
    availability_zone = ["eu-west-2a", "eu-west-2b"]
  }
}

variable "private_subnet" {
  description = "Values for Private Subnets"
  type = object({
    cidr_block        = list(string)
    availability_zone = list(string)
  })
  default = {
    cidr_block        = ["10.0.11.0/24", "10.0.21.0/24"]
    availability_zone = ["eu-west-2a", "eu-west-2b"]
  }
}

variable "cidr_block_0" {
  description = "CIDR block with value '0.0.0.0/0'"
  type        = string
  default     = "0.0.0.0/0"
}