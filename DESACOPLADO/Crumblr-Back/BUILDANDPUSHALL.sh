#!/bin/bash
set -e

# === CONFIGURACIÓN GENERAL ===
AWS_REGION="us-east-1"
ACCOUNT_ID="992382705242"
REPOSITORIES=("create-crumb" "get-crumb" "get-crumbs" "update-crumb" "delete-crumb")

# === AUTENTICACIÓN ECR ===
echo "🔐 Autenticando con ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# === BUILD Y PUSH POR CADA LAMBDA ===
for repo in "${REPOSITORIES[@]}"; do
    echo "🚀 Construyendo imagen para ${repo}..."

    # Ir al directorio correspondiente
    cd lambda/functions/${repo}


    # Forzar formato Docker clásico y arquitectura compatible
    export DOCKER_BUILDKIT=0
    export DOCKER_DEFAULT_PLATFORM=linux/amd64

    # Construir la imagen
    docker build --platform linux/amd64 -t ${repo} .



    # Etiquetar para ECR
    docker tag ${repo}:latest ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${repo}:latest

    # Subir a ECR
    echo "⬆️  Subiendo ${repo} a ECR..."
    docker push ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${repo}:latest

    # Volver al root del proyecto
    cd ../../..
done

echo "✅ Todas las imágenes se construyeron y subieron correctamente."
