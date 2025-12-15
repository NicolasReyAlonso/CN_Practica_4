import json
import logging
from datetime import datetime
from shared.services.crumb_service import CrumbService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

service = CrumbService()

def handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    try:
        crumb_id = event['pathParameters']['id']
        crumb = service.get_crumb(crumb_id)
        
        crumb_dict = {
            'crumb_id': crumb.crumb_id,
            'content': crumb.content,
            'image_url': crumb.image_url,
            'created_at': crumb.created_at.isoformat() if isinstance(crumb.created_at, datetime) else crumb.created_at
        }
        
        response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,x-api-key",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
            },
            "body": json.dumps(crumb_dict)
        }
        return response
    except ValueError as e:
        return {
            "statusCode": 404,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,x-api-key",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
            },
            "body": json.dumps({"error": str(e)})
        }
    except Exception as e:
        logger.exception("Error getting crumb")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,x-api-key",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
            },
            "body": json.dumps({"error": str(e)})
        }