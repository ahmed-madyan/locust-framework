import os

# 2xx Success
OK = int(os.environ.get("OK", 200))
CREATED = int(os.environ.get("CREATED", 201))
ACCEPTED = int(os.environ.get("ACCEPTED", 202))
NO_CONTENT = int(os.environ.get("NO_CONTENT", 204))

# 3xx Redirection
MOVED_PERMANENTLY = int(os.environ.get("MOVED_PERMANENTLY", 301))
FOUND = int(os.environ.get("FOUND", 302))
NOT_MODIFIED = int(os.environ.get("NOT_MODIFIED", 304))

# 4xx Client Errors
BAD_REQUEST = int(os.environ.get("BAD_REQUEST", 400))
UNAUTHORIZED = int(os.environ.get("UNAUTHORIZED", 401))
FORBIDDEN = int(os.environ.get("FORBIDDEN", 403))
NOT_FOUND = int(os.environ.get("NOT_FOUND", 404))
METHOD_NOT_ALLOWED = int(os.environ.get("METHOD_NOT_ALLOWED", 405))
CONFLICT = int(os.environ.get("CONFLICT", 409))
UNPROCESSABLE_ENTITY = int(os.environ.get("UNPROCESSABLE_ENTITY", 422))
TOO_MANY_REQUESTS = int(os.environ.get("TOO_MANY_REQUESTS", 429))

# 5xx Server Errors
INTERNAL_SERVER_ERROR = int(os.environ.get("INTERNAL_SERVER_ERROR", 500))
BAD_GATEWAY = int(os.environ.get("BAD_GATEWAY", 502))
SERVICE_UNAVAILABLE = int(os.environ.get("SERVICE_UNAVAILABLE", 503))
GATEWAY_TIMEOUT = int(os.environ.get("GATEWAY_TIMEOUT", 504))
