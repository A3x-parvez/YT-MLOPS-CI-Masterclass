import subprocess
import time
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session", autouse=True)
def run_streamlit():
    # Start the app in the background
    process = subprocess.Popen(
        ["streamlit", "run", "app.py", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)  # wait for server to start
    yield
    process.terminate()

def test_calculator_all_results():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8501")

        # Enter the number 2
        page.fill("input[type=number]", "2")

        # Click "Calculate"
        page.click("button:has-text('Calculate')")

        # Wait for all results to appear and verify
        expected_results = [
            "2 raised to the power of  2  is : 4.",
            "2 raised to the power of  3  is : 8.",
            "2 raised to the power of  4  is : 16.",
            "2 raised to the power of  5  is : 32."
        ]

        for result in expected_results:
            page.wait_for_selector(f"text={result}")
            assert result in page.content()

        browser.close()
def test_calculator_invalid_input():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8501")

        # Enter an invalid input
        page.fill("input[type=number]", "invalid")

        # Click "Calculate"
        page.click("button:has-text('Calculate')")

        # Check for error message
        error_message = "Invalid input. Please enter a valid number."
        page.wait_for_selector(f"text={error_message}")
        assert error_message in page.content()

        browser.close()
