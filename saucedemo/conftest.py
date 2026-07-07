import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run the browser in headless mode",
    )
    parser.addoption(
        "--browsers",
        action="store",
        default="chrome,edge,firefox,opera",
        help="Comma-separated browsers for the browser_compatibility suite "
        "(chrome, edge, firefox, opera). Unavailable browsers are skipped.",
    )


@pytest.fixture
def driver(request):
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")
    # Selenium Manager (built into Selenium 4.6+) auto-downloads the matching chromedriver.
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
