# ==========|  NULL-RESOURCE  |==========

resource "null_resource" "build" {
  # ----| Resource builds Dockerfile locally and push it to AWS ECR

  provisioner "local-exec" {
    # Bash script, which build Dockerfile and push it to AWS ECR
    command     = var.script
    # Directory, where script is executed
    working_dir = var.working_dir

    # Variables for script execution
    environment = {
      TAG               = var.image_tag
      REPO_REGION       = var.aws_region
      ECR_REPO_URL      = var.ecr_repository_url
      APP_NAME          = var.app_name
      ENV_NAME          = var.environment
    }
  }
}