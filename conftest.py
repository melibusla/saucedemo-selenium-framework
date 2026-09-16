import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.test_data_loader import VALID_USER

BASE_URL = "https://www.saucedemo.com/"
TWO_PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]


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


@pytest.fixture()
def products_in_cart(driver):
    """Logs in as VALID_USER and adds TWO_PRODUCTS to the cart. Leaves the
    browser on the inventory page. Returns the product list so tests don't
    have to redeclare it."""
    login_page = LoginPage(driver)
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    inventory_page = InventoryPage(driver)
    for product in TWO_PRODUCTS:
        inventory_page.add_to_cart(product)
    return TWO_PRODUCTS


@pytest.fixture()
def checkout_step_one(driver, products_in_cart):
    """Builds on products_in_cart: navigates to the cart, then to checkout
    step one (the shipping info form). Returns the same product list."""
    InventoryPage(driver).go_to_cart()
    CartPage(driver).go_to_checkout()
    return products_in_cart
