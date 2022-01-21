# =========| LISTENER RULES |=========

resource "aws_lb_listener_rule" "http" {
  listener_arn = aws_lb_listener.http.arn
  priority     = var.listener_rule.priority

  condition {
    path_pattern {
      values = [var.listener_rule.path_pattern]
    }
  }

  action {
    type             = var.listener_rule.action_type
    target_group_arn = aws_lb_target_group.alb.arn
  }
}