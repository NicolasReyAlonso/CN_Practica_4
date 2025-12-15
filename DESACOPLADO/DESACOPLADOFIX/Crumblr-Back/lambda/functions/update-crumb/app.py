import json
import logging
from datetime import datetime
from shared.services.crumb_service import CrumbService

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

service = CrumbService()

def handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    try:
        crumb_id = event['pathParameters']['id']
        data = json.loads(event['body'])
        updated = service.update_crumb(crumb_id, data)
        
        # Convertir el objeto Crumb a dict serializable
        crumb_dict = {
            'crumb_id': updated.crumb_id,
            'content': updated.content,
            'image_url': updated.image_url,
            'created_at': updated.created_at.isoformat() if isinstance(updated.created_at, datetime) else updated.created_at
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
        logger.info(f"Response: {response}")
        return response
    except ValueError as e:
        logger.warning(f"Crumb not found: {crumb_id}")
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
        logger.exception("Error updating crumb")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,x-api-key",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
            },
            "body": json.dumps({"error": str(e)})
        }