# ==========| PUBLIC SUBNET |==========

resource "aws_subnet" "public" {
  count                   = length(var.public_subnet)
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.public_subnet.cidr_block[count.index]
  availability_zone       = var.public_subnet.availability_zone[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "Public Subnet ${count.index + 1} for ${var.app_name}-${var.environment}"
  }
}


# ==========| PRIVATE SUBNET |==========

resource "aws_subnet" "private" {
  count                   = length(var.private_subnet)
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.private_subnet.cidr_block[count.index]
  availability_zone       = var.private_subnet.availability_zone[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "Private Subnet ${count.index + 1} for ${var.app_name}-${var.environment}"
  }
}