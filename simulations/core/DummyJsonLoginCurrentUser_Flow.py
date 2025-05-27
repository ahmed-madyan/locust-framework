from locust import HttpUser, task, between

from config import HTTP_METHODS, BASE_PATHS, HEADERS, SERVICE_BASE_URI
from request_payloads.core.DummyJsonPayloads import DummyJsonPayloads
from simulations.base.base_load_shape import BaseLoadShape
from simulations.base.base_user import BaseTaskSet


class MyUserSet(BaseTaskSet):
    """Define Global Static Variables."""
    bearer_token = ""

    @task(1)
    def dummy_json_login(self):
        """Example task to get users."""
        # Build and execute request using configuration
        response = (self.request_builder
                    .with_url(BASE_PATHS["DUMMY_JSON_LOGIN"])
                    .with_method(HTTP_METHODS["POST"])
                    .with_headers(HEADERS["COMMON_HEADERS"])
                    .with_json(DummyJsonPayloads.LOGIN_PAYLOAD)
                    .with_name("Dummy Json Login")
                    .execute())
        self.bearer_token = response.json().get("accessToken")
        print(f"Bearer token: {self.bearer_token}")

    @task(2)
    def dummy_json_current_user(self):
        """Example task to get users."""
        # Build and execute request using configuration
        response = (self.request_builder
                    .with_url(BASE_PATHS["DUMMY_JSON_CURRENT_AUTH_USER"])
                    .with_method(HTTP_METHODS["GET"])
                    .with_headers({"Authorization": f"Bearer {self.bearer_token}"})
                    .with_name("Dummy Json current user")
                    .execute())


class CustomLoadShape(BaseLoadShape):
    pass


class MyUser(HttpUser):
    host = SERVICE_BASE_URI["DUMMY_JSON_BASE_URI"]
    wait_time = between(1, 5)
    tasks = [MyUserSet]
