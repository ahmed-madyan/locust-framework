# Locust Framework

A powerful and flexible framework for load testing and performance testing built on top of Locust. This framework provides a structured approach to creating, managing, and executing load tests with advanced features for request building, response validation, and load shaping.

---

## Table of Contents
- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
  - [Basic Example](#basic-example)
  - [Load Profile Example](#load-profile-example)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/locust-framework.git
   cd locust-framework
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Features

- **Request Builder:** Fluent API for building HTTP requests with support for all HTTP methods, headers, parameters, and body data.
- **Response Validator:** Comprehensive response validation including status codes, headers, JSON schema, and custom validations.
- **Load Shaper:** Advanced load profile management with support for:
  - Spike testing
  - Ramp-up scenarios
  - Steady-state testing
  - Stress testing
- **Logging Framework:** Detailed logging with:
  - Colored console output
  - Rotating file logs
  - Multiple log levels
  - Contextual information

---

## Usage

### Basic Example

This example demonstrates how to use the framework to build and validate a simple GET request.

```python
from locust import HttpUser, task, between
from request_builder import RequestBuilder
from response_validator import ResponseValidator
from load_shaper import LoadProfileFactory

class MyUser(HttpUser):
    wait_time = between(1, 2)
    
    def on_start(self):
        self.request_builder = RequestBuilder(self)
        self.validator = ResponseValidator()
    
    @task
    def get_users(self):
        # Configure validations
        validator = self.validator.reset() \
            .expect_status_code(200) \
            .expect_json_schema(user_schema)
        
        # Build and execute request
        response = (self.request_builder
            .with_url("/api/users")
            .with_method("GET")
            .with_headers({"Accept": "application/json"})
            .with_params({"page": "1"})
            .with_name("Get Users")
            .execute())
        
        # Validate response
        validator.assert_valid(response)
```

### Load Profile Example

This example shows how to define a custom load profile for your test.

```python
from load_shaper import LoadProfileFactory

# Create a load profile
load_profile = LoadProfileFactory() \
    .spike(10) \                    # Initial spike of 10 users
    .ramp_up(50, 30) \             # Ramp up to 50 users over 30 seconds
    .steady_users(50, 60) \        # Maintain 50 users for 60 seconds
    .stress_ramp(50, 100, 30) \    # Stress test from 50 to 100 users
    .build()
```

---

## Project Structure

```
locust-framework/
├── logger/               # Logging framework
├── request_builder/      # Request building utilities
├── response_validator/   # Response validation tools
├── load_shaper/          # Load profile management
└── config/               # Configuration files
```

---

## Configuration

The framework uses a modular configuration system. Key configuration files are located in the `config/` directory:

- **BaseURI.py**: Defines base URLs for services.
- **Schema.py**: Contains JSON schemas for response validation.
- **LoadShaperConfig.py**: Load test configuration parameters.
- **LoadProfiles.py**: Predefined load profiles for tests.
- **Headers.py**: Common HTTP headers used in requests.
- **BasePath.py**: API endpoint paths.
- **RequestMethod.py**: Supported HTTP method configurations.
- **StatusCode.py**: HTTP status code definitions.
- **Parameters.py**: Common request parameters.

---

## Logging

The framework includes a comprehensive logging system. Example usage:

```python
from logger import logger

# Different log levels
logger.debug("Detailed debug info", some_var=value)
logger.info("Operation completed", result=result)
logger.warning("High memory usage", memory_usage="85%")
logger.error("Request failed", error=str(e))
logger.critical("System crash imminent", reason="Memory overflow")
```

Logs are written to both:
- **Console** (with colors for different levels)
- **Rotating log files** in the `logs/` directory

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## Acknowledgments

- Built on top of [Locust](https://locust.io/)
- Inspired by various load testing frameworks and best practices 