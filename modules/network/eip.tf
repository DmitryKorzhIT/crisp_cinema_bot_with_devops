# =========| EIP |=========

resource "aws_eip" "nat_gateway" {
  count  = var.count_value
  vpc    = true

  tags   = {
    Name = "EIP ${count.index + 1} for ${var.app_name}-${var.environment}"
  }
}