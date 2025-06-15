from playwright.sync_api import sync_playwright
import time

def capture_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:3000/login")
        page.fill("input[name=username]", "admin")
        page.fill("input[name=password]", "admin")
        page.click("button[type=submit]")
        time.sleep(5)
        page.goto("http://localhost:3000/d/c10e3d52-cc2e-461c-8a07-63e8278b2960/locust-load-test-dashboard")
        time.sleep(10)
        page.screenshot(path="grafana-screenshot.png")
        browser.close()

if __name__ == "__main__":
    capture_screenshot() 