from typing import Dict

# HTTP Methods
HTTP_METHODS = {
    "GET": "GET",
    "POST": "POST",
    "PUT": "PUT",
    "DELETE": "DELETE",
    "PATCH": "PATCH",
    "HEAD": "HEAD",
    "OPTIONS": "OPTIONS"
}

# Method Configurations
METHOD_CONFIGS = {
    "GET": {
        "requires_body": False,
        "idempotent": True,
        "cacheable": True
    },
    "POST": {
        "requires_body": True,
        "idempotent": False,
        "cacheable": False
    },
    "PUT": {
        "requires_body": True,
        "idempotent": True,
        "cacheable": False
    },
    "DELETE": {
        "requires_body": False,
        "idempotent": True,
        "cacheable": False
    },
    "PATCH": {
        "requires_body": True,
        "idempotent": False,
        "cacheable": False
    }
}

# Method Default Headers
METHOD_HEADERS = {
    "GET": {
        "Accept": "application/json"
    },
    "POST": {
        "Content-Type": "application/json",
        "Accept": "application/json"
    },
    "PUT": {
        "Content-Type": "application/json",
        "Accept": "application/json"
    },
    "DELETE": {
        "Accept": "application/json"
    },
    "PATCH": {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
} 