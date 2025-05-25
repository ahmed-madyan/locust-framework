from typing import Dict

# HTTP Status Codes
STATUS_CODES = {
    # 2xx Success
    "OK": 200,
    "CREATED": 201,
    "ACCEPTED": 202,
    "NO_CONTENT": 204,
    
    # 3xx Redirection
    "MOVED_PERMANENTLY": 301,
    "FOUND": 302,
    "NOT_MODIFIED": 304,
    
    # 4xx Client Errors
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "METHOD_NOT_ALLOWED": 405,
    "CONFLICT": 409,
    "UNPROCESSABLE_ENTITY": 422,
    "TOO_MANY_REQUESTS": 429,
    
    # 5xx Server Errors
    "INTERNAL_SERVER_ERROR": 500,
    "BAD_GATEWAY": 502,
    "SERVICE_UNAVAILABLE": 503,
    "GATEWAY_TIMEOUT": 504
}

# Status Code Categories
STATUS_CATEGORIES = {
    "success": [200, 201, 202, 204],
    "redirection": [301, 302, 304],
    "client_error": [400, 401, 403, 404, 405, 409, 422, 429],
    "server_error": [500, 502, 503, 504]
}

# Expected Status Codes for Methods
EXPECTED_STATUS_CODES = {
    "GET": {
        "success": [200, 304],
        "error": [400, 401, 403, 404, 429, 500]
    },
    "POST": {
        "success": [201, 202],
        "error": [400, 401, 403, 409, 422, 429, 500]
    },
    "PUT": {
        "success": [200, 204],
        "error": [400, 401, 403, 404, 409, 422, 429, 500]
    },
    "DELETE": {
        "success": [200, 204],
        "error": [400, 401, 403, 404, 409, 429, 500]
    },
    "PATCH": {
        "success": [200, 204],
        "error": [400, 401, 403, 404, 409, 422, 429, 500]
    }
} 