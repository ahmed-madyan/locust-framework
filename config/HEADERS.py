# Common Headers
COMMON_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# API Specific Headers
REQ_RES_API_KEY_HEADERS = {
    "x-api-key": "reqres-free-v1"
}

# Authentication Headers
AUTH_HEADERS = {
    "Authorization": "Bearer "  # Template for token-based auth
}

# Custom Headers
CUSTOM_HEADERS = {
    "X-Custom-Header": "custom-value"
}

# Combine all headers
HEADERS = {
    "REQ_RES_API_KEY_HEADERS": REQ_RES_API_KEY_HEADERS,
    "COMMON_HEADERS": COMMON_HEADERS,
    "AUTH_HEADERS": AUTH_HEADERS
} 