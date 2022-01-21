# =========| TARGET GROUPS |=========

resource "aws_lb_target_group" "alb" {
  name        = "target-group-${var.app_name}-${var.environment}"
  port        = var.server_port
  protocol    = var.protocol_http
  vpc_id      = var.vpc_id # out
  target_type = var.target_type

  health_check {
    path                 = var.health_check_path
    protocol             = var.protocol_http
    matcher              = var.health_check_matcher
    interval             = 15
    timeout              = 3
    healthy_threshold    = 2
    unhealthy_threshold  = 2
  }
}