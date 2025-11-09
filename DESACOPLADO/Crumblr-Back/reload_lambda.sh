#!/bin/bash
AWS_REGION="us-east-1"
ACCOUNT_ID="992382705242"
echo "actualizando lambdas"
aws lambda update-function-code --function-name get-crumbs --image-uri ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/get-crumbs:latest
aws lambda update-function-code --function-name create-crumb --image-uri ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/create-crumb:latest
aws lambda update-function-code --function-name get-crumb --image-uri ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/get-crumb:latest
aws lambda update-function-code --function-name update-crumb --image-uri ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/update-crumb:latest
aws lambda update-function-code --function-name delete-crumb --image-uri ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/delete-crumb:latest