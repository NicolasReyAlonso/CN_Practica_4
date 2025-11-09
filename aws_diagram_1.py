# diagrams script for the Crumblr architecture described by the user
# Requires: pip install diagrams
# and graphviz installed on the system.

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS
from diagrams.aws.network import ELB, NLB
from diagrams.aws.database import RDS
from diagrams.aws.network import APIGateway
from diagrams.aws.general import Client
from diagrams.onprem.compute import Server
from diagrams.aws.security import Shield as SecurityGroup


# Notes:
# - diagrams' node names / modules vary slightly by version. If an import fails,
#   try `from diagrams.aws.network import ALB` or `from diagrams.aws.apigateway import Apigateway`
#   or inspect diagrams package nodes (docs: https://diagrams.mingrammer.com).
# - This script is a conceptual diagram matching the CloudFormation you pasted:
#   - 1 Postgres DB (RDS)
#   - Backend ECS Fargate behind a Network Load Balancer (internal) + API Gateway (VPC LINK)
#   - Frontend ECS Fargate behind an Internet-facing Application Load Balancer

with Diagram("Crumblr - ECS Fargate + API Gateway + PostgreSQL", show=False, filename="crumblr_architecture", direction="TB"):
    user = Client("Internet User")

    # FRONTEND (public)
    with Cluster("Frontend VPC / Public subnets"):
        frontend_sg = SecurityGroup("Frontend SG\nAllow: 80 HTTP")
        frontend_alb = ELB("Frontend ALB\n(internet-facing)")
        with Cluster("Frontend ECS (Fargate)"):
            frontend_task = ECS("Frontend task\n(crumblr-frontend)")

    # BACKEND (private)
    with Cluster("Backend VPC / Private subnets"):
        backend_sg = SecurityGroup("Backend SG\nAllow: 8080 from NLB / API Gateway")
        # internal NLB targets backend tasks (ip target type)
        backend_nlb = NLB("Backend NLB\n(internal)")
        with Cluster("Backend ECS (Fargate)"):
            backend_task = ECS("Backend task\n(crumblr-service)\nEnv: DB_TYPE, DB_HOST,...")

        # VPC Link for API Gateway -> NLB
        vpc_link = Server("VPC Link")

    # DATABASE (private)
    with Cluster("Database (private)"):
        postgres = RDS("Postgres RDS\n(crumblr-db)")

    # API Gateway (public) that proxies to internal NLB via VPC Link
    api_gw = APIGateway("API Gateway\n(crumblr-api)")

    # Connections: user -> frontend ALB -> frontend tasks
    user >> Edge(label="HTTP 80") >> frontend_alb >> Edge(label="target: frontend task (80)") >> frontend_task

    # Frontend calls API Gateway (configured with API_URL/API_KEY)
    frontend_task >> Edge(label="calls API (API_URL)") >> api_gw

    # API Gateway -> VPC Link -> NLB -> Backend tasks
    api_gw >> Edge(label="VPC_LINK (HTTP proxy)") >> vpc_link >> backend_nlb >> Edge(label="targets (port 8080)") >> backend_task

    # Backend -> Postgres
    backend_task >> Edge(label="TCP 5432") >> postgres

    # NLB healthcheck path /health and security group relationships
    # (diagram notes)

    # Optional: show log groups / ECR as servers
    with Cluster("CI / ECR / Logging"):
        ecr = Server("ECR: crumblr-repo")
        logs = Server("CloudWatch Logs\n(/ecs/crumblr-service, /ecs/crumbler-frontend)")

    # depict relations
    frontend_task >> logs
    backend_task >> logs
    frontend_task >> ecr
    backend_task >> ecr

    # Expose outputs conceptually
    # (e.g., FrontendALB.DNSName, API Gateway URL, API Key)

# End of script
