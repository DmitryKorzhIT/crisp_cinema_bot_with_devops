# ==========| VPS |==========

resource "aws_vpc" "vpc" {
  cidr_block              = var.vpc.cidr_block
  instance_tenancy        = var.vpc.instance_tenancy
  enable_dns_hostnames    = var.vpc.enable_dns_hostnames

  tags = {
    Name    = "VPC for ${var.app_name}-${var.environment}"
  }
}