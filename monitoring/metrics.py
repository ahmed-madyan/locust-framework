from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Request metrics
REQUEST_COUNT = Counter(
    'locust_request_count',
    'Number of requests made',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'locust_request_latency_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)

# User metrics
ACTIVE_USERS = Gauge(
    'locust_active_users',
    'Number of active users'
)

# Response size metrics
RESPONSE_SIZE = Histogram(
    'locust_response_size_bytes',
    'Response size in bytes',
    ['method', 'endpoint']
)

# Error metrics
ERROR_COUNT = Counter(
    'locust_error_count',
    'Number of errors',
    ['method', 'endpoint', 'error_type']
)

def start_metrics_server(port=9646):
    """Start the Prometheus metrics server"""
    start_http_server(port)

class MetricsMiddleware:
    """Middleware to collect metrics for each request"""
    
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        start_time = time.time()
        method = environ.get('REQUEST_METHOD', '')
        path = environ.get('PATH_INFO', '')

        def custom_start_response(status, headers, exc_info=None):
            status_code = status.split()[0]
            REQUEST_COUNT.labels(method=method, endpoint=path, status=status_code).inc()
            
            # Record latency
            latency = time.time() - start_time
            REQUEST_LATENCY.labels(method=method, endpoint=path).observe(latency)
            
            # Record response size if available
            content_length = next((int(h[1]) for h in headers if h[0].lower() == 'content-length'), 0)
            if content_length:
                RESPONSE_SIZE.labels(method=method, endpoint=path).observe(content_length)
            
            return start_response(status, headers, exc_info)

        try:
            return self.app(environ, custom_start_response)
        except Exception as e:
            ERROR_COUNT.labels(method=method, endpoint=path, error_type=type(e).__name__).inc()
            raise 