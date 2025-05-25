"""
RequestBuilder module for constructing and executing HTTP requests in a fluent interface style.
This module provides a builder pattern implementation for creating HTTP requests with various
configurations including headers, parameters, body data, and more.

The RequestBuilder supports:
- All standard HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Header management
- Query parameter handling
- JSON and form data body support
- Request naming for Locust statistics
- Comprehensive logging
- Error handling
"""

from typing import Dict, Any, Optional, Union
from locust import HttpUser, User, TaskSet, SequentialTaskSet
import json
from urllib.parse import urljoin
from logger import logger

class RequestBuilder:
    """
    A fluent interface builder for constructing and executing HTTP requests.
    
    This class provides a chainable API for building HTTP requests with various
    configurations. It integrates with Locust's HTTP client for making requests
    and includes comprehensive logging and error handling.
    
    Example usage:
        builder = RequestBuilder(user)
        response = (builder
            .with_host("https://api.example.com")
            .with_url("/users")
            .with_method("GET")
            .with_headers({"Accept": "application/json"})
            .with_params({"page": 1})
            .with_name("Get Users")
            .execute())
    """
    
    def __init__(self, client: Union[User, HttpUser, TaskSet, SequentialTaskSet]):
        """
        Initialize the RequestBuilder with a Locust client.
        
        Args:
            client (Union[User, HttpUser, TaskSet, SequentialTaskSet]): 
                The Locust client instance to make requests with. This can be any
                of the supported Locust client types.
        """
        self.client = client
        # Initialize all request parameters with default values
        self._headers: Dict[str, str] = {}
        self._params: Dict[str, Any] = {}
        self._data: Optional[Union[Dict[str, Any], str]] = None
        self._json: Optional[Dict[str, Any]] = None
        self._method: str = "GET"
        self._url: str = ""
        self._name: str = ""
        self._host: str = ""
        logger.debug("RequestBuilder initialized", client_type=type(client).__name__)

    def with_host(self, host: str) -> 'RequestBuilder':
        """
        Set the host URL for the request.
        
        Args:
            host (str): The base host URL (e.g., 'https://api.example.com')
            
        Returns:
            RequestBuilder: The builder instance for method chaining
        """
        self._host = host.rstrip('/')
        logger.debug("Host set", host=host)
        return self

    def with_url(self, url: str) -> 'RequestBuilder':
        """
        Set the request URL path.
        
        Args:
            url (str): The URL path (e.g., '/users' or '/api/v1/products')
            
        Returns:
            RequestBuilder: The builder instance for method chaining
        """
        self._url = url.lstrip('/')
        logger.debug("URL set", url=url)
        return self

    def with_method(self, method: str) -> 'RequestBuilder':
        """
        Set the HTTP method for the request.
        
        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE', 'PATCH')
            
        Returns:
            RequestBuilder: The builder instance for method chaining
        """
        self._method = method.upper()
        logger.debug("Method set", method=method)
        return self

    def with_headers(self, headers: Dict[str, str]) -> 'RequestBuilder':
        """
        Set or update request headers.
        
        Args:
            headers (Dict[str, str]): Dictionary of header names and values
            
        Returns:
            RequestBuilder: The builder instance for method chaining
        """
        self._headers.update(headers)
        logger.debug("Headers updated", headers=headers)
        return self

    def with_params(self, params: Dict[str, Any]) -> 'RequestBuilder':
        """
        Set or update URL query parameters.
        
        Args:
            params (Dict[str, Any]): Dictionary of parameter names and values
            
        Returns:
            RequestBuilder: The builder instance for method chaining
        """
        self._params.update(params)
        logger.debug("Parameters updated", params=params)
        return self

    def with_data(self, data: Union[Dict[str, Any], str]) -> 'RequestBuilder':
        """
        Set the request body data (for form data or raw content).
        
        Args:
            data (Union[Dict[str, Any], str]): The request body data
            
        Returns:
            RequestBuilder: The builder instance for method chaining
        """
        self._data = data
        logger.debug("Data set", data_type=type(data).__name__)
        return self

    def with_json(self, json_data: Dict[str, Any]) -> 'RequestBuilder':
        """
        Set the JSON request body.
        
        Args:
            json_data (Dict[str, Any]): The JSON data to send in the request body
            
        Returns:
            RequestBuilder: The builder instance for method chaining
        """
        self._json = json_data
        logger.debug("JSON data set", data_type=type(json_data).__name__)
        return self

    def with_name(self, name: str) -> 'RequestBuilder':
        """
        Set a name for the request (used in Locust statistics).
        
        Args:
            name (str): A descriptive name for the request
            
        Returns:
            RequestBuilder: The builder instance for method chaining
        """
        self._name = name
        logger.debug("Request name set", name=name)
        return self

    def _get_http_client(self):
        """
        Get the appropriate HTTP client based on the client type.
        
        Returns:
            The HTTP client instance to use for making requests
        """
        if isinstance(self.client, (TaskSet, SequentialTaskSet)):
            return self.client.user.client
        return self.client.client

    def _log_response(self, response: Any) -> None:
        """
        Log detailed information about the response.
        
        This method logs:
        - Basic response info (status code, response time, content length)
        - Response headers
        - Response content (as JSON if possible, otherwise as text)
        - Response cookies
        
        Args:
            response: The response object from the request
        """
        try:
            # Log basic response info
            logger.info("Response received",
                       status_code=response.status_code,
                       response_time=response.elapsed.total_seconds(),
                       content_length=len(response.content) if hasattr(response, 'content') else 0)

            # Log response headers
            if hasattr(response, 'headers'):
                logger.debug("Response headers", headers=dict(response.headers))

            # Log response content
            if hasattr(response, 'content'):
                try:
                    # Try to parse as JSON
                    content = response.json()
                    logger.debug("Response content (JSON)", content=content)
                except json.JSONDecodeError:
                    # If not JSON, log as text
                    content = response.text
                    # Truncate long content
                    if len(content) > 1000:
                        content = content[:1000] + "... (truncated)"
                    logger.debug("Response content (text)", content=content)

            # Log response cookies if any
            if hasattr(response, 'cookies'):
                logger.debug("Response cookies", cookies=dict(response.cookies))

        except Exception as e:
            logger.error("Error logging response", error=str(e))

    def execute(self) -> Any:
        """
        Execute the request with all configured parameters.
        
        This method:
        1. Validates the request configuration
        2. Constructs the full URL
        3. Prepares request parameters
        4. Executes the request using the appropriate HTTP method
        5. Logs the response details
        6. Returns the response object
        
        Returns:
            The response object from the request
            
        Raises:
            ValueError: If the URL is not set or an unsupported HTTP method is used
            Exception: For any other errors during request execution
        """
        if not self._url:
            error_msg = "URL must be set before executing the request"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Construct the full URL
        full_url = self._url
        if self._host:
            full_url = urljoin(f"{self._host}/", self._url)

        # Prepare the request parameters
        kwargs = {
            "headers": self._headers,
            "params": self._params,
            "name": self._name or full_url
        }

        # Add body data if present
        if self._json is not None:
            kwargs["json"] = self._json
        elif self._data is not None:
            kwargs["data"] = self._data

        logger.info("Executing request", 
                   method=self._method,
                   url=full_url,
                   name=self._name,
                   has_json=self._json is not None,
                   has_data=self._data is not None)

        try:
            # Get the appropriate HTTP client
            http_client = self._get_http_client()
            
            # Execute the request based on the method
            method = self._method.lower()
            if method == "get":
                response = http_client.get(full_url, **kwargs)
            elif method == "post":
                response = http_client.post(full_url, **kwargs)
            elif method == "put":
                response = http_client.put(full_url, **kwargs)
            elif method == "delete":
                response = http_client.delete(full_url, **kwargs)
            elif method == "patch":
                response = http_client.patch(full_url, **kwargs)
            else:
                error_msg = f"Unsupported HTTP method: {method}"
                logger.error(error_msg)
                raise ValueError(error_msg)

            # Log detailed response information
            self._log_response(response)
            return response

        except Exception as e:
            logger.error("Request failed", 
                        error=str(e),
                        method=self._method,
                        url=full_url)
            raise

    def reset(self) -> 'RequestBuilder':
        """
        Reset all request parameters to their default values.
        
        This method is useful when you want to reuse the builder for a new request
        without creating a new instance.
        
        Returns:
            RequestBuilder: The builder instance for method chaining
        """
        self._headers = {}
        self._params = {}
        self._data = None
        self._json = None
        self._method = "GET"
        self._url = ""
        self._name = ""
        self._host = ""
        logger.debug("RequestBuilder reset")
        return self 