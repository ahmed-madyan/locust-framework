# Locust Monitoring with Prometheus and Grafana

## Quick Start Guide

1. **Install Docker Desktop**
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and restart computer
   - Verify Docker is running (check system tray)

2. **Install Dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Start Services** (in separate terminals)
   ```bash
   # Terminal 1: Start monitoring stack
   cd monitoring
   docker-compose up -d

   # Terminal 2: Start exporter
   cd monitoring
   python locust_exporter.py

   # Terminal 3: Start Locust
   locust -f your_test_file.py
   ```

4. **Configure Grafana**
   - Open http://localhost:3000
   - Login: admin/admin
   - Add Prometheus data source:
     - URL: http://prometheus:9090
     - Access: Server
   - Import dashboard:
     - Click "+" > Import
     - Enter ID: 11985
     - Click "Load"

5. **Verify Setup**
   - Check Prometheus: http://localhost:9090/targets
   - Check Grafana dashboard for metrics
   - Run a Locust test to see live data

## Troubleshooting

- If metrics don't appear:
  1. Check Docker is running
  2. Verify exporter shows "Started locust exporter on port 9646"
  3. Check Prometheus targets page
  4. Verify Grafana data source connection

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
   - Use dashboard ID: 11985 (Locust Dashboard)

## Available Metrics

The exporter provides various metrics including:
- Number of users (locust_users)
- Requests per second (locust_requests_per_second)
- Failures per second (locust_failures_per_second)
- Response time percentiles (locust_response_time_percentile) 