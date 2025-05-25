"""
Example User class demonstrating how to use the Locust Framework for load testing.
This file shows how to create a user class that simulates real user behavior by making
HTTP requests to an API and validating the responses.
"""

from locust import HttpUser, task, between
from request_builder.RequestBuilder import RequestBuilder
from reponse_validator.ResponseValidator import ResponseValidator


class ExampleUser(HttpUser):
    """
    A Locust user class that simulates API interactions.
    This class demonstrates how to:
    1. Initialize request builders and validators
    2. Define common validation rules
    3. Create tasks that simulate user actions
    4. Validate API responses
    """
    
    # Define wait time between tasks (1-3 seconds) to simulate real user behavior
    wait_time = between(1, 3)
    
    def on_start(self):
        """
        Initialize user-specific data when the user starts.
        This method is called once when each simulated user starts.
        """
        # Initialize the request builder with the current user instance
        self.RequestBuilder = RequestBuilder(self)
        # Set the base URL for all requests
        self.RequestBuilder.with_host("https://api.example.com")
        
        # Initialize response validator for checking API responses
        self.validator = ResponseValidator()
        
        # Define common validations that apply to all requests
        self.validator.expect_header("Content-Type", "application/json")
        
        # Define JSON schema for user data validation
        self.user_schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"}
            },
            "required": ["id", "name", "email"]
        }
    
    @task
    def get_users(self):
        """
        Task to simulate retrieving a list of users.
        This demonstrates how to:
        1. Set up request-specific validations
        2. Build and execute a GET request
        3. Validate the response
        """
        # Configure validations specific to this request
        validator = self.validator.reset()\
            .expect_status_code(200)\
            .expect_json_path("data.0.id", None)  # Ensure at least one user exists
        
        # Build and execute the request using the fluent API
        response = (self.RequestBuilder
            .with_url("/api/users")
            .with_method("GET")
            .with_headers({"Accept": "application/json"})
            .with_name("Get Users")
            .execute())
        
        # Validate the response against our expectations
        validator.assert_valid(response)
        
        # Process response if needed
        users = response.json()
        # Do something with users
    
    @task
    def create_user(self):
        """
        Task to simulate creating a new user.
        This demonstrates how to:
        1. Prepare request data
        2. Set up request-specific validations
        3. Build and execute a POST request
        4. Validate the response
        """
        # Prepare the user data for creation
        user_data = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        
        # Configure validations specific to this request
        validator = self.validator.reset()\
            .expect_status_code(201)\
            .expect_json_schema(self.user_schema)
        
        # Build and execute the request using the fluent API
        response = (self.RequestBuilder
            .with_url("/api/users")
            .with_method("POST")
            .with_headers({
                "Content-Type": "application/json",
                "Accept": "application/json"
            })
            .with_json(user_data)
            .with_name("Create User")
            .execute())
        
        # Validate the response against our expectations
        validator.assert_valid(response)
        
        # Process response if needed
        created_user = response.json()
        # Do something with created user 