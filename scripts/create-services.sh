#!/bin/bash

set -e

AWS_REGION="ap-south-1"

CLUSTER="fullstack-cluster-v3"

BACKEND_SERVICE="backend-service-v3"
FRONTEND_SERVICE="frontend-service-v3"

BACKEND_TASK=$1
FRONTEND_TASK=$2

BACKEND_TG="arn:aws:elasticloadbalancing:ap-south-1:327481844909:targetgroup/backend-tg-v3/0405b1469fa21cfb"

FRONTEND_TG="arn:aws:elasticloadbalancing:ap-south-1:327481844909:targetgroup/frontend-tg-v3/ebf4b5e6e03aeba1"

SUBNET1="subnet-03072c4aa2899b691"
SUBNET2="subnet-0f39577a1220c32c6"

SECURITY_GROUP="sg-0b2e468fdb0a891f4"

echo "Creating Backend Service..."

aws ecs create-service \
  --cluster $CLUSTER \
  --service-name $BACKEND_SERVICE \
  --task-definition $BACKEND_TASK \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET1,$SUBNET2],securityGroups=[$SECURITY_GROUP],assignPublicIp=ENABLED}" \
  --load-balancers targetGroupArn=$BACKEND_TG,containerName=backend,containerPort=5000

echo "Creating Frontend Service..."

aws ecs create-service \
  --cluster $CLUSTER \
  --service-name $FRONTEND_SERVICE \
  --task-definition $FRONTEND_TASK \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET1,$SUBNET2],securityGroups=[$SECURITY_GROUP],assignPublicIp=ENABLED}" \
  --load-balancers targetGroupArn=$FRONTEND_TG,containerName=frontend,containerPort=3000

echo "Services created successfully."
