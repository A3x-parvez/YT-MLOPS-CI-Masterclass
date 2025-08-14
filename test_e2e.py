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
        page.goto("http://localhost:8501", wait_until="networkidle")

        input_box = page.locator("input[type=number]")
        input_box.fill("")
        input_box.type("2")

        page.click("button:has-text('Calculate')")
        page.wait_for_selector("div:has-text('raised to the power')")

        result_elements = page.locator("div:has-text('raised to the power')")
        all_results = "\n".join(
            [result_elements.nth(i).inner_text() for i in range(result_elements.count())]
        )

        expected_results = [
            "2 raised to the power of  2  is : 4.",
            "2 raised to the power of  3  is : 8.",
            "2 raised to the power of  4  is : 16.",
            "2 raised to the power of  5  is : 32."
        ]
        for result in expected_results:
            assert result in all_results

        browser.close()
