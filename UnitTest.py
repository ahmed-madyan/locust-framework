from locust import HttpUser, task, between

from config import PARAMETERS, STATUS_CODES, HTTP_METHODS, BASE_PATHS, HEADERS, SCHEMAS, \
    SERVICE_BASE_URI
from simulations.base.base_load_shape import BaseLoadShape
from simulations.base.base_user import BaseTaskSet


class MyUser(BaseTaskSet):
    host = SERVICE_BASE_URI["REQ_RES_BASE_URI"]
    wait_time = between(1, 2)

    @task
    def get_users(self):
        """Example task to get users."""
        # Get request configuration from endpoints
        # request_config = ENDPOINTS["users"]["methods"]["get_users"]

        # Configure validations for this specific request
        validator = self.validator.reset() \
            .expect_status_code(STATUS_CODES["OK"]) \
            .expect_json_schema(SCHEMAS["USER_LIST_RESPONSE_SCHEMA"])

        # Build and execute request using configuration
        response = (self.request_builder
                    .with_url(BASE_PATHS["REQ_RES_USERS_LIST_BASE_PATHS"])
                    .with_method(HTTP_METHODS["GET"])
                    .with_headers(HEADERS["REQ_RES_API_KEY_HEADERS"])
                    .with_params(PARAMETERS["REQ_RES_PAGE_PARAMS"])
                    .with_name("Get Users")
                    .execute())

        # print(F"ResponseValidator: {validator.assert_valid(response)}")
        #
        # if response.status_code == STATUS_CODES["OK"]:
        #     print(F"Passed with status code {STATUS_CODES["OK"]}")
        #     print(response.content)


class CustomLoadShape(BaseLoadShape):
    pass


class UserClass(HttpUser):
    host = SERVICE_BASE_URI["REQ_RES_BASE_URI"]
    wait_time = between(1, 2)
    tasks = [MyUser]
