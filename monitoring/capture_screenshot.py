from playwright.sync_api import sync_playwright, TimeoutError
import time
import sys
import socket
import requests

def check_port(host, port, timeout=5):
    """Check if a port is open on the given host."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error checking port {port} on {host}: {str(e)}")
        return False

def wait_for_grafana(page, max_retries=5, retry_delay=10):
    """Wait for Grafana to be ready by checking the login page."""
    # Try different hostnames
    hosts = ["localhost", "grafana", "127.0.0.1"]
    port = 3000
    
    for host in hosts:
        print(f"\nTrying to connect to Grafana at {host}:{port}")
        if check_port(host, port):
            print(f"Port {port} is open on {host}")
            for attempt in range(max_retries):
                try:
                    print(f"Attempt {attempt + 1}/{max_retries} to connect to Grafana...")
                    url = f"http://{host}:{port}/login"
                    print(f"Connecting to {url}")
                    page.goto(url, timeout=30000)
                    # Wait for the login form to be visible
                    page.wait_for_selector("input[name=username]", timeout=10000)
                    print("Grafana login page is ready!")
                    return True
                except TimeoutError as e:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < max_retries - 1:
                        print(f"Waiting {retry_delay} seconds before next attempt...")
                        time.sleep(retry_delay)
                    else:
                        print(f"Max retries reached for {host}. Trying next host...")
                        break
        else:
            print(f"Port {port} is not open on {host}")
    
    print("All hosts failed. Grafana might not be ready or accessible.")
    return False

def capture_screenshot():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Wait for Grafana to be ready
            if not wait_for_grafana(page):
                print("Failed to connect to Grafana. Exiting...")
                sys.exit(1)
            
            # Login to Grafana
            print("Logging into Grafana...")
            page.fill("input[name=username]", "admin")
            page.fill("input[name=password]", "admin")
            page.click("button[type=submit]")
            
            # Wait for login to complete
            print("Waiting for login to complete...")
            time.sleep(5)
            
            # Navigate to dashboard
            print("Navigating to dashboard...")
            page.goto("http://localhost:3000/d/c10e3d52-cc2e-461c-8a07-63e8278b2960/locust-load-test-dashboard")
            
            # Wait for dashboard to load
            print("Waiting for dashboard to load...")
            time.sleep(10)
            
            # Take screenshot
            print("Taking screenshot...")
            page.screenshot(path="grafana-screenshot.png")
            print("Screenshot saved successfully!")
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    capture_screenshot() 