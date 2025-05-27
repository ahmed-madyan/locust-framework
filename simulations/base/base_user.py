from locust import SequentialTaskSet
from request_builder.RequestBuilder import RequestBuilder
from reponse_validator.ResponseValidator import ResponseValidator
from config import SERVICE_BASE_URI


class BaseTaskSet(SequentialTaskSet):
    """Base class for all TaskSet implementations that provides common initialization logic."""

    def on_start(self):
        """Initialize any user-specific data when the user starts."""
        self.request_builder = RequestBuilder(self)
        self.request_builder.with_host(SERVICE_BASE_URI["DUMMY_JSON_BASE_URI"])
        # Set the host URL once during initialization
        self.validator = ResponseValidator()
