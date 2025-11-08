aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 992382705242.dkr.ecr.us-east-1.amazonaws.com
docker build -t get-crumb .
docker tag get-crumb:latest 992382705242.dkr.ecr.us-east-1.amazonaws.com/get-crumb:latest
docker push 992382705242.dkr.ecr.us-east-1.amazonaws.com/get-crumb:latest