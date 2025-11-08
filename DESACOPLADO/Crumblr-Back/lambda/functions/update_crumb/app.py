import json
from shared.services.crumb_service import CrumbService

service = CrumbService()

def handler(event, context):
    try:
        crumb_id = event['pathParameters']['crumb_id']
        data = json.loads(event['body'])
        updated = service.update_crumb(crumb_id, data)
        return {"statusCode": 200, "body": json.dumps(updated.__dict__)}
    except ValueError as e:
        return {"statusCode": 404, "body": json.dumps({"error": str(e)})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
