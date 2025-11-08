import json
from shared.services.crumb_service import CrumbService

service = CrumbService()

def handler(event, context):
    try:
        data = json.loads(event['body'])
        crumb = service.create_crumb(data)
        return {"statusCode": 201, "body": json.dumps(crumb.__dict__)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
