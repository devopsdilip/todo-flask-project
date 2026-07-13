#!/bin/bash

set -e

IMAGE_TAG=$1

AWS_REGION="ap-south-1"
AWS_ACCOUNT_ID="327481844909"

BACKEND_REPO="backend-v3"
FRONTEND_REPO="frontend-v3"

CLUSTER="fullstack-cluster-v3"

BACKEND_SERVICE="backend-service-v3"
FRONTEND_SERVICE="frontend-service-v3"

echo "Downloading latest task definitions..."

aws ecs describe-task-definition \
    --task-definition backend-task \
    --query taskDefinition \
    > backend-task.json

aws ecs describe-task-definition \
    --task-definition frontend-task \
    --query taskDefinition \
    > frontend-task.json

echo "Updating backend image..."

BACKEND_IMAGE="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$BACKEND_REPO:$IMAGE_TAG"

jq --arg IMAGE "$BACKEND_IMAGE" \
'.containerDefinitions[0].image=$IMAGE
| del(
.taskDefinitionArn,
.revision,
.status,
.requiresAttributes,
.compatibilities,
.registeredAt,
.registeredBy
)' \
backend-task.json > backend-new.json

echo "Updating frontend image..."

FRONTEND_IMAGE="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$FRONTEND_REPO:$IMAGE_TAG"

BACKEND_URL="http://fullstack-alb-v3-8216980.ap-south-1.elb.amazonaws.com"

jq \
  --arg IMAGE "$FRONTEND_IMAGE" \
  --arg BACKEND "$BACKEND_URL" \
'
.containerDefinitions[0].image=$IMAGE
|
(.containerDefinitions[0].environment[] | select(.name=="BACKEND_URL")).value=$BACKEND
|
del(
.taskDefinitionArn,
.revision,
.status,
.requiresAttributes,
.compatibilities,
.registeredAt,
.registeredBy
)
' \
frontend-task.json > frontend-new.json

echo "Registering backend task..."

BACKEND_TASK_ARN=$(aws ecs register-task-definition \
    --cli-input-json file://backend-new.json \
    --query "taskDefinition.taskDefinitionArn" \
    --output text)

echo "Registering frontend task..."

FRONTEND_TASK_ARN=$(aws ecs register-task-definition \
    --cli-input-json file://frontend-new.json \
    --query "taskDefinition.taskDefinitionArn" \
    --output text)

echo "Checking if ECS services exist..."

BACKEND_EXISTS=$(aws ecs describe-services \
    --cluster $CLUSTER \
    --services $BACKEND_SERVICE \
    --query "failures" \
    --output text)

FRONTEND_EXISTS=$(aws ecs describe-services \
    --cluster $CLUSTER \
    --services $FRONTEND_SERVICE \
    --query "failures" \
    --output text)

if [[ -n "$BACKEND_EXISTS" ]] || [[ -n "$FRONTEND_EXISTS" ]]; then
    echo "ERROR: ECS services are missing."
    exit 1
fi

echo "Updating backend service..."

aws ecs update-service \
    --cluster $CLUSTER \
    --service $BACKEND_SERVICE \
    --task-definition $BACKEND_TASK_ARN \
    --force-new-deployment

echo "Updating frontend service..."

aws ecs update-service \
    --cluster $CLUSTER \
    --service $FRONTEND_SERVICE \
    --task-definition $FRONTEND_TASK_ARN \
    --force-new-deployment

echo "Waiting for backend..."

aws ecs wait services-stable \
    --cluster $CLUSTER \
    --services $BACKEND_SERVICE

echo "Waiting for frontend..."

aws ecs wait services-stable \
    --cluster $CLUSTER \
    --services $FRONTEND_SERVICE

echo "Deployment Successful!"
