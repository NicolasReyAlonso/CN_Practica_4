import json
from shared.services.crumb_service import CrumbService

service = CrumbService()

def handler(event, context):
    try:
        crumb_id = event['pathParameters']['crumb_id']
        crumb = service.get_crumb(crumb_id)
        return {"statusCode": 200, "body": json.dumps(crumb.__dict__)}
    except ValueError as e:
        return {"statusCode": 404, "body": json.dumps({"error": str(e)})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
