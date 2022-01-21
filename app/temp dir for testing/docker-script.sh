#!/bin/bash

# ================================================== #
# ========|   D O C K E R    S C R I P T   |======== #
# ================================================== #



echo "=============================================="
echo "==========| START SCRIPT EXECUTION |=========="
echo "=============================================="
echo ""

echo "========| Login AWS_ECR using Docker |========"
echo ""
aws ecr get-login-password --region $REPO_REGION | docker login --username AWS --password-stdin $ECR_REPO_URL
echo ""

echo "==========| Build Docker Container |=========="
echo ""
docker build -t $APP_NAME-$ENV_NAME:$TAG .
echo ""

echo "=============| Push to  AWS ECR |============="
echo ""
docker tag $APP_NAME-$ENV_NAME:$TAG $ECR_REPO_URL/$APP_NAME-$ENV_NAME:$TAG
docker push $ECR_REPO_URL/$APP_NAME-$ENV_NAME:$TAG
echo ""

echo ""
echo "============| SCRIPT HAS EXECUTED |==========="