from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from tests.test_data_loader import VALID_USER
from tests.test_data_loader import PROBLEM_USER
import pytest

# I1 — Sort by name A-Z
def test_sort_name_a_to_z(driver):
    login_page = LoginPage(driver)
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    inventory_page = InventoryPage(driver)
    inventory_page.sort_by("Name (A to Z)")
    displayed_names = inventory_page.get_displayed_names()
    assert displayed_names == sorted(displayed_names), "Products are not sorted A-Z"
    pass


# I2 — Sort by name Z-A
def test_sort_name_z_to_a(driver):
    login_page = LoginPage(driver)
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    inventory_page = InventoryPage(driver)
    inventory_page.sort_by("Name (Z to A)")
    displayed_names = inventory_page.get_displayed_names()
    assert displayed_names == sorted(displayed_names, reverse=True), "Products are not sorted Z-A"
    pass


# I3 — Sort by price low-high
def test_sort_price_low_to_high(driver):
    login_page = LoginPage(driver)
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    inventory_page = InventoryPage(driver)
    inventory_page.sort_by("Price (low to high)")
    displayed_prices = inventory_page.get_displayed_prices()
    assert displayed_prices == sorted(displayed_prices), "Products are not sorted low to high"
    pass


# I4 — Sort by price high-low
def test_sort_price_high_to_low(driver):
    login_page = LoginPage(driver)
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    inventory_page = InventoryPage(driver)
    inventory_page.sort_by("Price (high to low)")
    displayed_prices = inventory_page.get_displayed_prices()
    assert displayed_prices == sorted(displayed_prices, reverse=True), "Products are not sorted high to low"
    pass


# I5 — problem_user sort behavior (expected to be broken — test documents that)
@pytest.mark.xfail(reason="problem_user sort is deliberately broken on purpose")
def test_problem_user_sort_is_broken(driver):
    login_page = LoginPage(driver)
    login_page.login(PROBLEM_USER["username"], PROBLEM_USER["password"])
    inventory_page = InventoryPage(driver)
    inventory_page.sort_by("Price (high to low)")
    displayed_prices = inventory_page.get_displayed_prices()
    assert displayed_prices == sorted(displayed_prices, reverse=True), "Products are not sorted high to low"
    pass
