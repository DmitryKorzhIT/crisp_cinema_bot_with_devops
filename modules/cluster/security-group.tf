# ==========| SECURITY GROUP |==========

resource "aws_security_group" "http" {
  name        = "Security Group access to HTTP for ${var.app_name}-${var.environment}"
  description = "Enable HTTP access on Port 80"
  vpc_id      = var.vpc_id # out

  ingress {
    description = "HTTP Access"
    from_port   = var.server_port
    to_port     = var.server_port
    protocol    = var.protocol_tcp
    cidr_blocks = [var.cidr_block_0]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.cidr_block_0]
  }

  tags   = {
    Name = "Security Group access to HTTP for ${var.app_name}-${var.environment}"
  }
}