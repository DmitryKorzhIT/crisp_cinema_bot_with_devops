# ==========| INITIALIZING GLOBAL VARIABLES |==========

variable app_name {}
variable environment {}
variable server_port {}


# ==========| VARIABLES FOR "BALANCER" MODULE |==========

variable "load_balancer_type" {
  description = "Load Balancer type"
  type        = string
  default     = "application"
}

variable "protocol_http" {
  description = "Protocol 'HTTP'"
  type        = string
  default     = "HTTP"
}

variable "target_type" {
  description = "Target type"
  type        = string
  default     = "ip"
}

variable "health_check_path" {
  description = "Health check path '/'"
  type        = string
  default     = "/"
}

variable "health_check_matcher" {
  description = "Response code '200' for HTTP"
  type        = string
  default     = "200"
}

variable "listener_fixed_response" {
  description = "Values for Fixed Response"
  type = object({
    type         = string
    content_type = string
    message_body = string
    status_code  = number
  })
  default = {
    type         = "fixed-response"
    content_type = "text/plain"
    message_body = "404: page not found"
    status_code  = 404
  }
}

variable "listener_rule" {
  description = "Values for Listener Rule"
  type = object({
    priority     = number
    path_pattern = string
    action_type  = string
  })
  default = {
    priority     = 100
    path_pattern = "*"
    action_type  = "forward"
  }
}


# ==========|  IMPORT VARIABLES FROM OTHER MODULES  |==========

variable "vpc_id" {
  description = "VPC ID"
  type        = string
  default     = null
}

variable "public_subnets_id" {
  description = "Public Subnets ID"
  type        = list(string)
  default     = null
}

variable "security_group_id" {
  description = "Security Group ID"
  type        = string
  default     = null
}