# =========| INTERNET GATEWAY |=========

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id

  tags      = {
    Name    = "Internet Gateway for ${var.app_name}-${var.environment}"
  }
}