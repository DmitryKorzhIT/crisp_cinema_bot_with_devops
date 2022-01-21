# =========| NAT GATEWAYS |=========

resource "aws_nat_gateway" "nat_gateway" {
  count         = var.count_value
  allocation_id = element(aws_eip.nat_gateway.*.id, count.index)
  subnet_id     = element(aws_subnet.public.*.id, count.index)

  tags   = {
    Name = "NAT Gateway Public Subnet ${count.index + 1} for ${var.app_name}-${var.environment}"
  }
}