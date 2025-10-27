#!/bin/zsh
source ./.env.sh

STACKNAME="TicketsECR"
APPNAME=
aws cloudformation create-stack --stack-name $STACKNAME --template-body file://./ecr.yml
aws cloudformation wait stack-create-complete --stack-name $STACKNAME

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

ECR_URI=$(aws cloudformation describe-stacks \
  --stack-name $STACKNAME \
  --query "Stacks[0].Outputs[?OutputKey=='RepositoryUri'].OutputValue" \
  --output text)
docker