#!/bin/bash
source ./.env.sh

STACKNAME="TicketsECR"

# Crear el stack de CloudFormation
aws cloudformation create-stack \
  --stack-name $STACKNAME \
  --template-body file://./ecr.yml

# Esperar a que termine la creación
aws cloudformation wait stack-create-complete --stack-name $STACKNAME

# Obtener el URI y nombre del repositorio ECR desde los outputs
ECR_URI=$(aws cloudformation describe-stacks \
  --stack-name $STACKNAME \
  --query "Stacks[0].Outputs[?OutputKey=='RepositoryUri'].OutputValue" \
  --output text)

REP_NAME=$(aws cloudformation describe-stacks \
  --stack-name $STACKNAME \
  --query "Stacks[0].Outputs[?OutputKey=='RepositoryName'].OutputValue" \
  --output text)

# Verificar que no estén vacíos
if [ -z "$ECR_URI" ] || [ -z "$REP_NAME" ]; then
  echo "Error: No se pudo obtener el URI o nombre del repositorio ECR."
  exit 1
fi

echo "Repositorio ECR: $ECR_URI"
echo "Nombre del repo: $REP_NAME"

# Login en ECR
aws ecr get-login-password --region $AWS_REGION | \
docker login --username AWS --password-stdin $ECR_URI

# Build de la imagen Docker
docker build -t $REP_NAME -f ./Dockerfile .

docker tag "$REP_NAME" "${ECR_URI}:latest"
docker push "${ECR_URI}:latest"
IMAGE_NAME="${ECR_URI}:latest"

DB_ENDPOINT=${DB_ENDPOINT:-""}

cat > ./db_params.json <<EOF
[
  {
    "ParameterKey": "DBName",
    "ParameterValue": "$DB_NAME"
  },
  {
    "ParameterKey": "DBUser",
    "ParameterValue": "$DB_USER"
  },
  {
    "ParameterKey": "DBPassword",
    "ParameterValue": "$DB_PASS"
  },
  {
    "ParameterKey": "VpcId",
    "ParameterValue": "$VPC_ID"
  },
  {
    "ParameterKey": "SubnetIds",
    "ParameterValue": "$AWS_SUBNET_IDS"
  }
]
EOF

#ECR
if [[ "$DB_TYPE" == "postgres" ]]; then
  aws cloudformation create-stack \
    --stack-name $RDS_STACK \
    --template-body file://./db_postgres.yml \
    --parameters file://./db_params.json

  echo "Esperando a que se cree la DB..."
  aws cloudformation wait stack-create-complete --stack-name $RDS_STACK

  # Obtener outputs de la DB
  DB_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name $RDS_STACK \
    --query "Stacks[0].Outputs[?OutputKey=='DBEndpoint'].OutputValue" \
    --output text)

  DB_PORT=$(aws cloudformation describe-stacks \
    --stack-name $RDS_STACK \
    --query "Stacks[0].Outputs[?OutputKey=='DBPort'].OutputValue" \
    --output text)

  echo "Base de datos creada correctamente: ""$DB_ENDPOINT"":""$DB_PORT"
fi

cat > ./main_params.json <<EOF
[
  {
    "ParameterKey": "ImageName",
    "ParameterValue": "$DIMAGE_NAME"
  },
  {
    "ParameterKey": "VpcId",
    "ParameterValue": "$VPC_ID"
  },
  {
    "ParameterKey": "DBType",
    "ParameterValue": "$DB_TYPE"
  },
  {
    "ParameterKey": "SubnetIds",
    "ParameterValue": "$AWS_SUBNET_IDS"
  },
  {
    "ParameterKey": "DBHost",
    "ParameterValue": "$DB_ENDPOINT"
  },
  {
    "ParameterKey": "DBName",
    "ParameterValue": "$DB_NAME"
  },
  {
    "ParameterKey": "DBUser",
    "ParameterValue": "$DB_USER"
  },
  {
    "ParameterKey": "DBPass",
    "ParameterValue": "$DB_PASS"
  }
]
EOF

aws cloudformation create-stack \
  --stack-name $APP_STACK_NAME \
  --template-body file://./main.yml \
  --parameters file://./main_params.json

  echo "Esperando a que se cree la APP"
  aws cloudformation wait stack-create-complete --stack-name $RDS_STACK