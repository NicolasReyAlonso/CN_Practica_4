import json
from shared.services.crumb_service import CrumbService

service = CrumbService()

def handler(event, context):
    try:
        crumbs = service.get_all_crumbs()
        return {
            "statusCode": 200,
            "body": json.dumps([c.__dict__ for c in crumbs])
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
