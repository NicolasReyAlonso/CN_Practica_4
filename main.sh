#!/bin/zsh
source ./.env.sh

STACKNAME="TicketsECR"

# Crear el stack de CloudFormation
aws cloudformation create-stack \
  --stack-name $STACKNAME \
  --template-body file://./ecr.yml \
  --capabilities CAPABILITY_IAM

# Esperar a que termine la creación
aws cloudformation wait stack-create-complete --stack-name $STACKNAME

# Obtener el URI del repositorio ECR desde los outputs
ECR_URI=$(aws cloudformation describe-stacks \
  --stack-name $STACKNAME \
  --query "Stacks[0].Outputs[?OutputKey=='RepositoryUri'].OutputValue" \
  --output text)

echo "Repositorio ECR: $ECR_URI"

# Login en ECR usando el URI obtenido
aws ecr get-login-password --region $AWS_REGION | \
docker login --username AWS --password-stdin $ECR_URI

# Build de la imagen Docker
docker build -t $IMAGE_NAME -f ./Dockerfile . --provenance false

# Taggear la imagen con el URI del ECR
docker tag $IMAGE_NAME $ECR_URI:latest

# Push de la imagen al ECR
docker push $ECR_URI:latest
