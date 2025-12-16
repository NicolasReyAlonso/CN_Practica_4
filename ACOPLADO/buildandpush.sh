aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 992382705242.dkr.ecr.us-east-1.amazonaws.com
docker build -t crumblr-repo . --platform linux/amd64 --provenance false
docker tag crumblr-repo:latest 992382705242.dkr.ecr.us-east-1.amazonaws.com/crumblr-repo:latest
docker push 992382705242.dkr.ecr.us-east-1.amazonaws.com/crumblr-repo:latest