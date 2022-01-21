# =========| LISTENERS |=========

resource "aws_lb_listener" "http" {
  load_balancer_arn  = aws_lb.alb.arn
  port               = var.server_port
  protocol           = var.protocol_http

  # Default return empty page with code 404
  default_action {
    type = var.listener_fixed_response.type

    fixed_response {
      content_type = var.listener_fixed_response.content_type
      message_body = var.listener_fixed_response.message_body
      status_code  = var.listener_fixed_response.status_code
    }
  }
}