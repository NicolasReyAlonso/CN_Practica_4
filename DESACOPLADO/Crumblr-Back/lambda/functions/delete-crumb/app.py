import json
import logging
from shared.services.crumb_service import CrumbService

# Configurar logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

service = CrumbService()

def handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    try:
        crumb_id = event['pathParameters']['id']
        service.delete_crumb(crumb_id)
        response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,x-api-key",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
            },
            "body": json.dumps({"message": "Crumb deleted successfully"})
        }
        logger.info(f"Response: {response}")
        return response
    except ValueError as e:
        logger.warning(f"Crumb not found: {e}")
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
        logger.exception("Error deleting crumb")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,x-api-key",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
            },
            "body": json.dumps({"error": str(e)})
        }