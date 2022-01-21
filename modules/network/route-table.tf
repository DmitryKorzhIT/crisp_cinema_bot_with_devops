# =========| ROUTE TABLE FOR PUBLIC |=========

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = var.cidr_block_0
    gateway_id = aws_internet_gateway.internet_gateway.id
  }

  tags = {
    Name = "Public Route Table for ${var.app_name}-${var.environment}"
  }
}


# =========| ROUTE TABLE FOR PRIVATE |=========

resource "aws_route_table" "private" {
  count  = var.count_value
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block      = var.cidr_block_0
    nat_gateway_id  = element(aws_nat_gateway.nat_gateway.*.id, count.index)
  }

  tags   = {
    Name = "Private Route Table ${count.index + 1} for ${var.app_name}-${var.environment}"
  }
}