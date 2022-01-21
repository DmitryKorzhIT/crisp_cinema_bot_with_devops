[
  {
    "name": "${container_name}",
    "image": "${app_image}",
    "cpu": ${fargate_cpu},
    "memory": ${fargate_memory},
    "networkMode": "awsvpc",
    "portMappings": [
    {
      "containerPort": ${app_port},
    "hostPort": ${app_port}
  }
],
  "environment": [
  {
    "name": "VERSION",
    "value": "${image_tag}"
  }
]
  }
]