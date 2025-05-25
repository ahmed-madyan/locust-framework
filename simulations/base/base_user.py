from locust import SequentialTaskSet
from request_builder.RequestBuilder import RequestBuilder
from reponse_validator.ResponseValidator import ResponseValidator


class BaseTaskSet(SequentialTaskSet):
    """Base class for all TaskSet implementations that provides common initialization logic."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bearer_token = None

    def on_start(self, host=None):
        """Initialize any user-specific data when the user starts."""
        self.request_builder = RequestBuilder(self)
        # Set the host URL once during initialization
        self.request_builder.with_host(self.host)
        self.validator = ResponseValidator() 