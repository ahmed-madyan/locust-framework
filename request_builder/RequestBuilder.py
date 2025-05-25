from typing import Dict, Any, Optional, Union
from locust import HttpUser, task
import json
from urllib.parse import urljoin
from logger import logger

class RequestBuilder:
    def __init__(self, client: HttpUser):
        """
        Initialize the RequestBuilder with a Locust HttpUser client.
        
        Args:
            client (HttpUser): The Locust HttpUser instance to make requests with
        """
        self.client = client
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
        """
        self._host = host.rstrip('/')
        logger.debug("Host set", host=host)
        return self

    def with_url(self, url: str) -> 'RequestBuilder':
        """Set the request URL."""
        self._url = url.lstrip('/')
        logger.debug("URL set", url=url)
        return self

    def with_method(self, method: str) -> 'RequestBuilder':
        """Set the HTTP method."""
        self._method = method.upper()
        logger.debug("Method set", method=method)
        return self

    def with_headers(self, headers: Dict[str, str]) -> 'RequestBuilder':
        """Set request headers."""
        self._headers.update(headers)
        logger.debug("Headers updated", headers=headers)
        return self

    def with_params(self, params: Dict[str, Any]) -> 'RequestBuilder':
        """Set URL parameters."""
        self._params.update(params)
        logger.debug("Parameters updated", params=params)
        return self

    def with_data(self, data: Union[Dict[str, Any], str]) -> 'RequestBuilder':
        """Set request body data."""
        self._data = data
        logger.debug("Data set", data_type=type(data).__name__)
        return self

    def with_json(self, json_data: Dict[str, Any]) -> 'RequestBuilder':
        """Set JSON request body."""
        self._json = json_data
        logger.debug("JSON data set", data_type=type(json_data).__name__)
        return self

    def with_name(self, name: str) -> 'RequestBuilder':
        """Set a name for the request (useful for Locust statistics)."""
        self._name = name
        logger.debug("Request name set", name=name)
        return self

    def _log_response(self, response: Any) -> None:
        """Log detailed response information."""
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
        Execute the request with the configured parameters.
        
        Returns:
            The response from the request
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
            # Execute the request based on the method
            method = self._method.lower()
            if method == "get":
                response = self.client.client.get(full_url, **kwargs)
            elif method == "post":
                response = self.client.client.post(full_url, **kwargs)
            elif method == "put":
                response = self.client.client.put(full_url, **kwargs)
            elif method == "delete":
                response = self.client.client.delete(full_url, **kwargs)
            elif method == "patch":
                response = self.client.client.patch(full_url, **kwargs)
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
        """Reset all request parameters to their default values."""
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