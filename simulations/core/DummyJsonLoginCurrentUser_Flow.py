from locust import LoadTestShape, HttpUser, task, between
from typing import Optional, Tuple
from load_shaper.LoadProfileFactory import LoadProfileFactory
from request_builder.RequestBuilder import RequestBuilder
from reponse_validator.ResponseValidator import ResponseValidator
from config import PARAMETERS, STATUS_CODES, HTTP_METHODS, BASE_PATHS, HEADERS, LOAD_SHAPER_CONFIG, SCHEMAS, \
    SERVICE_BASE_URI
from request_payloads.DummyJsonPayloads import DummyJsonPayloads


class MyUser(HttpUser):
    host = SERVICE_BASE_URI["DUMMY_JSON_BASE_URI"]
    wait_time = between(1, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bearer_token = None

    def on_start(self, host=None):
        """Initialize any user-specific data when the user starts."""
        self.request_builder = RequestBuilder(self)
        # Set the host URL once during initialization
        self.request_builder.with_host(self.host)
        self.validator = ResponseValidator()

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


class CustomLoadShape(LoadTestShape):
    """
    A custom load shape that implements a complex load pattern using multiple phases:
    - Initial spike
    - Ramp up
    - Steady state
    - Stress test
    """

    def __init__(self) -> None:
        """Initialize the load shape with predefined phases."""
        super().__init__()
        config = LOAD_SHAPER_CONFIG
        self.phases = LoadProfileFactory() \
            .spike(config["INITIAL_SPIKE_USERS"]) \
            .build()
        # .ramp_up(config["RAMP_UP_USERS"], config["RAMP_UP_DURATION"]) \
        # .steady_users(config["STEADY_USERS"], config["STEADY_DURATION"]) \
        # .stress_ramp(config["STRESS_START_USERS"], config["STRESS_END_USERS"], config["STRESS_DURATION"]) \
        # .build()

    def tick(self) -> Optional[Tuple[int, float]]:
        """
        Calculate the number of users and spawn rate for the current time.

        Returns:
            Optional[Tuple[int, float]]: A tuple of (user_count, spawn_rate) or None if no phase is active
        """
        run_time = self.get_run_time()

        for phase in self.phases:
            user_count = phase.user_count_at(run_time)
            if user_count is not None:
                return (user_count, phase.spawn_rate)

        return None
