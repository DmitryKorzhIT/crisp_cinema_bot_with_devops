# ==========| ROUTE TABLE ASSOCIATION FOR PUBLIC |==========

resource "aws_route_table_association" "public_subnet" {
  count               = var.count_value
  subnet_id           = element(aws_subnet.public.*.id, count.index)
  route_table_id      = aws_route_table.public.id
}


# ==========| ROUTE TABLE ASSOCIATION FOR PRIVATE |==========

resource "aws_route_table_association" "private_subnet" {
  count          = var.count_value
  subnet_id      = element(aws_subnet.private.*.id, count.index)
  route_table_id = element(aws_route_table.private.*.id, count.index)
}