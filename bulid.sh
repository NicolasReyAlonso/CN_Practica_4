aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 992382705242.dkr.ecr.us-east-1.amazonaws.com
docker build -t cn/nicorepo -f ./Dockerfile . --platform linux/amd64 --provenance false
docker tag cn/nicorepo:latest 992382705242.dkr.ecr.us-east-1.amazonaws.com/cn/nicorepo:latest
docker push 992382705242.dkr.ecr.us-east-1.amazonaws.com/cn/nicorepo:latest