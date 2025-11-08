import json
from shared.services.crumb_service import CrumbService

service = CrumbService()

def handler(event, context):
    try:
        crumb_id = event['pathParameters']['crumb_id']
        service.delete_crumb(crumb_id)
        return {"statusCode": 204, "body": ""}
    except ValueError as e:
        return {"statusCode": 404, "body": json.dumps({"error": str(e)})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
