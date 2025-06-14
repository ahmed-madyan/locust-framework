from locust import HttpUser, task, between

from reponse_validator.ResponseValidator import ResponseValidator
from request_payloads.core.DummyJsonPayloads import DummyJsonPayloads
from simulations.base.base_load_shape import BaseLoadShape
from simulations.base.base_user import SequentialBaseTaskSet
from config import BaseURI, BasePath, RequestMethod, StatusCode, Headers


class MyUserSet(SequentialBaseTaskSet):
    """Define Global Static Variables."""
    bearer_token = ""

    @task(1)
    def dummy_json_login(self):
        """Example task to get users."""
        # Build and execute request using configuration
        response = (self.request_builder
                    .with_url(BasePath.DUMMY_JSON_LOGIN)
                    .with_method(RequestMethod.POST)
                    .with_headers(Headers.COMMON_HEADERS)
                    .with_json(DummyJsonPayloads.LOGIN_PAYLOAD)
                    .with_name("Dummy Json Login")
                    .execute())
        self.bearer_token = response.json().get("accessToken")
        validator = ResponseValidator().expect_status_code(StatusCode.OK)
        validator.validate(response)
        print(f"Bearer token: {self.bearer_token}")

    @task(2)
    def dummy_json_current_user(self):
        """Example task to get users."""
        # Build and execute request using configuration
        response = (self.request_builder
                    .with_url(BasePath.DUMMY_JSON_CURRENT_AUTH_USER)
                    .with_method(RequestMethod.GET)
                    .with_headers({"Authorization": f"Bearer {self.bearer_token}"})
                    .with_name("Dummy Json current user")
                    .execute())


class CustomLoadShape(BaseLoadShape):
    pass


class MyUser(HttpUser):
    host = BaseURI.REQ_RES_BASE_URI
    wait_time = between(1, 5)
    tasks = [MyUserSet]
