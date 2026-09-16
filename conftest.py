import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

BASE_URL = "https://www.saucedemo.com/"


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome or firefox",
    )


@pytest.fixture()
def driver(request):
    browser_name = request.config.getoption("browser_name")
    # Force headless for local runs to avoid browser UI prompts
    headless = True

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    # No implicit wait — mixing implicit and explicit waits causes
    # unpredictable delays (e.g. it waits out the full timeout when
    # checking that an element is absent). Page objects that need to
    # wait for something use an explicit WebDriverWait instead.
    driver.maximize_window()
    driver.get(BASE_URL)

    yield driver

    driver.quit()
