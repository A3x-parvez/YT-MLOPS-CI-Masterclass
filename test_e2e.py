import subprocess
import time
import socket
import pytest
from playwright.sync_api import sync_playwright

def wait_for_port(host, port, timeout=30):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Port {port} not available after {timeout} seconds")

@pytest.fixture(scope="session", autouse=True)
def run_streamlit():
    process = subprocess.Popen(
        [
            "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.port", "8501"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    wait_for_port("localhost", 8501, timeout=60)  # Wait until server is ready
    yield
    process.terminate()

def test_calculator_all_results():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Open the app
        page.goto("http://localhost:8501", wait_until="networkidle")

        # Fill the number input
        input_box = page.locator("input[type=number]")
        input_box.fill("")
        input_box.type("2")

        # Click the calculate button
        page.click("button:has-text('Calculate')")

        # Wait for one of the results to appear (timeout set to 10 seconds)
        page.wait_for_selector("div:has-text('squared is')", timeout=10000)

        # Get full HTML content for checking results
        content = page.content()

        # Remove all spaces for comparison to avoid spacing/formatting issues
        content_no_spaces = content.replace(" ", "")

        # Expected results based on your Streamlit app
        expected_results = [
            "2 squared is 4",
            "2 cubed is 8",
            "2 to the fourth power is 16",
            "2 to the fifth power is 32"
        ]

        # Assert each expected text is present (ignoring spaces)
        for expected in expected_results:
            assert expected.replace(" ", "") in content_no_spaces, \
                f"Expected '{expected}' in page content"

        browser.close()
