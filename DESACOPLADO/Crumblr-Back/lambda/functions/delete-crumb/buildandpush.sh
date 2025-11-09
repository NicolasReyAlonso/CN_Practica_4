aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 992382705242.dkr.ecr.us-east-1.amazonaws.com
docker build -t delete-crumb . --provenance false
docker tag delete-crumb:latest 992382705242.dkr.ecr.us-east-1.amazonaws.com/delete-crumb:latest
docker push 992382705242.dkr.ecr.us-east-1.amazonaws.com/delete-crumb:latest