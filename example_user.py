from locust import HttpUser, task, between
from request_builder.RequestBuilder import RequestBuilder
from reponse_validator.ResponseValidator import ResponseValidator



class ExampleUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    def on_start(self):
        """Initialize any user-specific data when the user starts."""
        self.RequestBuilder = RequestBuilder(self)
        # Set the host URL once during initialization
        self.RequestBuilder.with_host("https://api.example.com")
        
        # Initialize response validator
        self.validator = ResponseValidator()
        
        # Define common validations
        self.validator.expect_header("Content-Type", "application/json")
        
        # Define user schema
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
        """Example task to get users."""
        # Configure validations for this specific request
        validator = self.validator.reset()\
            .expect_status_code(200)\
            .expect_json_path("data.0.id", None)  # Ensure at least one user exists
        
        response = (self.RequestBuilder
            .with_url("/api/users")
            .with_method("GET")
            .with_headers({"Accept": "application/json"})
            .with_name("Get Users")
            .execute())
        
        # Validate the response
        validator.assert_valid(response)
        
        # Process response if needed
        users = response.json()
        # Do something with users
    
    @task
    def create_user(self):
        """Example task to create a user."""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        
        # Configure validations for this specific request
        validator = self.validator.reset()\
            .expect_status_code(201)\
            .expect_json_schema(self.user_schema)
        
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
        
        # Validate the response
        validator.assert_valid(response)
        
        # Process response if needed
        created_user = response.json()
        # Do something with created user 