# diagrams script for Crumblr decoupled architecture (Lambda + API Gateway + PostgreSQL/DynamoDB + ECS Frontend)
# Requires: pip install diagrams and graphviz installed on system.

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.aws.general import Client
from diagrams.aws.management import Cloudwatch
from diagrams.aws.devtools import Codebuild as ECR
from diagrams.aws.network import ELB
from diagrams.aws.security import Shield as SecurityGroup
from diagrams.aws.compute import ECS

with Diagram("Crumblr - Decoupled Lambda + API Gateway + Frontend", show=False, filename="crumblr_architecture_decoupled", direction="TB"):
    user = Client("Internet User")

    # FRONTEND (ECS + ALB)
    with Cluster("Frontend (ECS Fargate + ALB)"):
        frontend_sg = SecurityGroup("Frontend SG\nAllow: 80 HTTP")
        alb = ELB("Application Load Balancer\n(internet-facing)")
        with Cluster("Frontend ECS Service"):
            frontend = ECS("Frontend Task\ncrumblr-frontend")

    # API & LAMBDAS
    with Cluster("Serverless Backend (Lambdas)"):
        create_lambda = Lambda("create-crumb")
        get_lambda = Lambda("get-crumb")
        getall_lambda = Lambda("get-crumbs")
        update_lambda = Lambda("update-crumb")
        delete_lambda = Lambda("delete-crumb")

        lambdas = [create_lambda, get_lambda, getall_lambda, update_lambda, delete_lambda]

    api = APIGateway("API Gateway\n(crumblr-api)")

    # DATABASES
    with Cluster("Databases"):
        postgres = RDS("PostgreSQL\n(crumblr_db)")
        dynamo = Dynamodb("DynamoDB\n(crumbs)")

    # LOGGING / ECR
    with Cluster("Support Services"):
        cw = Cloudwatch("CloudWatch Logs\n(/aws/lambda/*, /ecs/crumbler-frontend)")
        ecr = ECR("ECR Repos\n(create-crumb, get-crumb, update-crumb, ...)")

    # CONNECTIONS
    user >> Edge(label="HTTP 80") >> alb >> frontend
    frontend >> Edge(label="API_URL / API_KEY") >> api
    api >> Edge(label="Invoke (AWS_PROXY)") >> lambdas
    for fn in lambdas:
        fn >> Edge(label="Read/Write") >> postgres
        fn >> Edge(label="Alt. DB option") >> dynamo
        fn >> cw
        fn >> ecr

    frontend >> cw
    frontend >> ecr
