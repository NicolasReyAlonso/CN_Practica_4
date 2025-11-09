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
        data = json.loads(event.get('body', '{}'))
        crumb = service.create_crumb(data)
        
        # Convertir el objeto Crumb a dict serializable
        crumb_dict = {
            'crumb_id': crumb.crumb_id,
            'content': crumb.content,
            'image_url': crumb.image_url,
            'created_at': crumb.created_at.isoformat() if isinstance(crumb.created_at, datetime) else crumb.created_at
        }
        
        response = {
            "statusCode": 201,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,x-api-key",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
            },
            "body": json.dumps(crumb_dict)
        }
        logger.info(f"Response: {response}")
        return response
    except Exception as e:
        logger.exception("Error creating crumb")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,x-api-key",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
            },
            "body": json.dumps({"error": str(e)})
        }