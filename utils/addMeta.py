import logging
from datetime import datetime 
logger = logging.getLogger("app")


def add_metadata(users):
    logger.info("added metadata success")
    return {
        "event": "user_list",
        "users": users,
        "message_id": "abc123",  # Can be dynamically generated if needed
        "correlation_id": "txn456",  # Can be dynamically generated if needed
        "status": "pending",
        "error_details": None,
        "retry_count": 0,
        "created_at": datetime.utcnow().isoformat() + "Z",  # Current timestamp
        "processed_at": None,
        "service_name": "user_service",
        "payload_version": "1.0"
    }