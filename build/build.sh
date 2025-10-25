TARGETNAME="cn/tickets-app"
aws cloudformation create-stack --stack-name TicketsECR --template-body file://../ecr.yml
docker build  --platform linux/amd64 -t $TARGETNAME -f ../Dockerfile . 
