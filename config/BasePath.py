import os

REQ_RES_USERS_LIST = os.environ.get("REQ_RES_USERS_LIST", "/api/users")
DUMMY_JSON_LOGIN = os.environ.get("DUMMY_JSON_LOGIN", "/auth/login")
DUMMY_JSON_CURRENT_AUTH_USER = os.environ.get("DUMMY_JSON_CURRENT_AUTH_USER", "/auth/me")
