import os
import json

COMMON_HEADERS = json.loads(os.environ.get("COMMON_HEADERS",
    '{"Content-Type": "application/json", "Accept": "application/json"}'
))

AUTH_HEADERS = json.loads(os.environ.get("AUTH_HEADERS",
    '{"Authorization": "Bearer YOUR_DEFAULT_TOKEN"}'
))

CUSTOM_HEADERS = json.loads(os.environ.get("CUSTOM_HEADERS",
    '{"X-Custom-Header": "custom-value"}'
))

REQ_RES_API_KEY_HEADERS = json.loads(os.environ.get("REQ_RES_API_KEY_HEADERS",
    '{"x-api-key": "reqres-free-v1"}'
))