# Locust Monitoring with Prometheus and Grafana

This directory contains the configuration for monitoring Locust performance tests using Prometheus and Grafana.

## Prerequisites

1. Install Docker Desktop for Windows:
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and restart your computer
   - Make sure Docker Desktop is running

2. Install Python dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

## Setup Instructions

1. Start the monitoring stack:
   ```bash
   docker-compose up -d
   ```

2. Start the custom Locust exporter:
   ```bash
   python locust_exporter.py
   ```

3. Start your Locust test:
   ```bash
   locust -f your_test_file.py
   ```

## Accessing the Dashboards

- Grafana: http://localhost:3000 (default credentials: admin/admin)
- Prometheus: http://localhost:9090

## Setting up Grafana

1. Log in to Grafana (http://localhost:3000)
2. Add Prometheus as a data source:
   - URL: http://prometheus:9090
   - Access: Server (default)
3. Import the Locust dashboard:
   - Go to Dashboards > Import
   - Use dashboard ID: 2587 (Locust Dashboard)

## Available Metrics

The exporter provides various metrics including:
- Number of users (locust_users)
- Requests per second (locust_requests_per_second)
- Failures per second (locust_failures_per_second)
- Response time percentiles (locust_response_time_percentile)

## Troubleshooting

If metrics are not showing up:
1. Ensure Docker Desktop is running
2. Check if the exporter is running (should see "Started locust exporter on port 9646")
3. Check Prometheus targets (http://localhost:9090/targets)
4. Verify the Prometheus configuration in prometheus.yml
5. Check Grafana data source configuration 