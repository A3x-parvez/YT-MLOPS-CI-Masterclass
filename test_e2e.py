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

        # Set number input to 2 (clear first to avoid appending)
        input_box = page.locator("input[type=number]")
        input_box.fill("")  # clear
        input_box.type("2")

        # Click "Calculate"
        page.click("button:has-text('Calculate')")

        # Grab all the text from the results container
        page.wait_for_selector("div:has-text('raised to the power')")
        content = page.inner_text("div:has-text('raised to the power')")

        expected_results = [
            "2 raised to the power of  2  is : 4.",
            "2 raised to the power of  3  is : 8.",
            "2 raised to the power of  4  is : 16.",
            "2 raised to the power of  5  is : 32."
        ]
        for result in expected_results:
            assert result in content

        browser.close()