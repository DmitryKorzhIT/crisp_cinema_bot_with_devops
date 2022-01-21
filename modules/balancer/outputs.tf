# =========| OUTPUTS |=========

output "alb_dns_name" {
  value = aws_lb.alb.dns_name
}

output "lb_target_group_id" {
  value = aws_lb_target_group.alb.id
}

output "lb_listener" {
  value = aws_lb_listener.http
}