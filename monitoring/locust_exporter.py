from prometheus_client import start_http_server, Gauge, Counter
import requests
import time
import json

# Metrics
USERS = Gauge('locust_users', 'Number of users')
REQUESTS_PER_SECOND = Gauge('locust_requests_per_second', 'Requests per second')
FAILURES_PER_SECOND = Gauge('locust_failures_per_second', 'Failures per second')
RESPONSE_TIME_PERCENTILE = Gauge('locust_response_time_percentile', 'Response time percentile', ['percentile'])

def fetch_metrics(locust_host):
    try:
        response = requests.get(f"{locust_host}/stats/requests")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching metrics: {e}")
        return None

def update_metrics(metrics):
    if not metrics:
        return

    # Update user count
    USERS.set(metrics.get('user_count', 0))

    # Update request rates
    REQUESTS_PER_SECOND.set(metrics.get('total_rps', 0))
    FAILURES_PER_SECOND.set(metrics.get('total_fail_per_sec', 0))

    # Update response time percentiles
    for percentile in ['50', '66', '75', '80', '90', '95', '98', '99', '100']:
        RESPONSE_TIME_PERCENTILE.labels(percentile=percentile).set(
            metrics.get('response_time_percentiles', {}).get(percentile, 0)
        )

def main():
    # Start the Prometheus HTTP server
    start_http_server(9646)
    print("Started locust exporter on port 9646")

    locust_host = "http://localhost:8089"
    
    while True:
        metrics = fetch_metrics(locust_host)
        if metrics:
            update_metrics(metrics)
        time.sleep(1)

if __name__ == '__main__':
    main() 