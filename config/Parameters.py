import os
import json

REQ_RES_PAGE_PARAMS = json.loads(os.environ.get("REQ_RES_PAGE_PARAMS",
    '{"page": "2"}'
))