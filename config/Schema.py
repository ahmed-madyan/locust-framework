import os
import json
from typing import Dict, Any

USER_LIST_RESPONSE_SCHEMA: Dict[str, Any] = json.loads(os.environ.get(
    "USER_LIST_RESPONSE_SCHEMA",
    """
    {
        "type": "object",
        "properties": {
            "page": {"type": "integer"},
            "per_page": {"type": "integer"},
            "total": {"type": "integer"},
            "total_pages": {"type": "integer"},
            "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "email": {"type": "string", "format": "email"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "avatar": {"type": "string", "format": "uri"}
                    },
                    "required": ["id", "email", "first_name", "last_name", "avatar"]
                }
            },
            "support": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "format": "uri"},
                    "text": {"type": "string"}
                },
                "required": ["url", "text"]
            }
        },
        "required": ["page", "per_page", "total", "total_pages", "data", "support"]
    }
    """
))
