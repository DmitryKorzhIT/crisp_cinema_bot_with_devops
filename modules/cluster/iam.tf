# ==========| IAM |==========

resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "${var.app_name}-${var.environment}-${var.ecs_task_execution_role_name}"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_execution_role.json
}

resource "aws_iam_role_policy" "ecs_task_execution_role" {
  name_prefix = "ecs_iam_role_policy"
  role        = aws_iam_role.ecs_task_execution_role.id
  policy      = data.template_file.ecs_service_policy.rendered
}

resource "aws_iam_role" "ecs_task_role" {
  name               = "${var.app_name}-${var.environment}-${var.ecs_task_role_name}"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "ecs_task_role" {
  name = "${var.app_name}-${var.environment}-${var.ecs_task_role_name}"
  role = aws_iam_role.ecs_task_role.id
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:Get*",
                "s3:List*"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}