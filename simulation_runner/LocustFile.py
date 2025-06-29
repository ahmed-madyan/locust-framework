from locust import events
from prometheus_client import start_http_server, Counter, Summary
from simulations.core.DummyJsonLoginCurrentUser_Flow import MyUser

# Define Prometheus custom metrics
REQUEST_COUNT = Counter('custom_locust_request_count', 'Total number of successful requests')
REQUEST_FAILURE_COUNT = Counter('custom_locust_request_failure_count', 'Total number of failed requests')
REQUEST_LATENCY = Summary('custom_locust_request_latency_seconds', 'Request latency in seconds')


# Prometheus Metrics Server Initialization
@events.init.add_listener
def on_locust_init(environment, **kwargs):
    # Starts Prometheus metrics server on port 8000
    start_http_server(8000)


# Track requests and update metrics
@events.request.add_listener
def track_request(request_type, name, response_time, response_length, exception, **kwargs):
    if exception is None:
        REQUEST_COUNT.inc()
    else:
        REQUEST_FAILURE_COUNT.inc()
    REQUEST_LATENCY.observe(response_time / 1000.0)  # Convert ms to seconds
 