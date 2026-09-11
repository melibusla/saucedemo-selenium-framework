import pytest
import json
from pathlib import Path

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

test_data_path = Path(__file__).parent.parent / "data" / "logindata.json"
with test_data_path.open() as f:
    test_data = json.load(f)
    test_list = test_data["data"]

# L1 — Valid login (standard_user)
@pytest.mark.parametrize("test_list_item", [test_list[0]])  # Only the first item for now
def test_valid_login(driver, test_list_item):
    login_page = LoginPage(driver)
    login_page.login(test_list_item["username"], test_list_item["password"])
    assert InventoryPage(driver).is_loaded(), "Inventory page did not load after valid login"
    pass
# L2 — Locked-out user
@pytest.mark.parametrize("test_list_item", [test_list[1]])
def test_locked_out_user(driver, test_list_item):
    login_page = LoginPage(driver)
    login_page.login(test_list_item["username"], test_list_item["password"])
    assert login_page.get_error_message() == test_list_item["expected_error"], "Expected error message for locked-out user not displayed"


# L3 — Empty username
@pytest.mark.parametrize("test_list_item", [test_list[2]])
def test_empty_username(driver, test_list_item):
    login_page = LoginPage(driver)
    login_page.login(test_list_item["username"], test_list_item["password"])
    assert login_page.get_error_message() == test_list_item["expected_error"], "Expected error message for empty username not displayed"


# L4 — Empty password
@pytest.mark.parametrize("test_list_item", [test_list[3]])
def test_empty_password(driver, test_list_item):
    login_page = LoginPage(driver)
    login_page.login(test_list_item["username"], test_list_item["password"])
    assert login_page.get_error_message() == test_list_item["expected_error"], "Expected error message for empty password not displayed"


# L5 — Both fields empty
@pytest.mark.parametrize("test_list_item", [test_list[4]])
def test_both_fields_empty(driver, test_list_item):
    login_page = LoginPage(driver)
    login_page.login(test_list_item["username"], test_list_item["password"])
    assert login_page.get_error_message() == test_list_item["expected_error"], "Expected error message for both fields empty not displayed"


# L6 — Invalid username/password combo
@pytest.mark.parametrize("test_list_item", [test_list[5]])
def test_invalid_credentials(driver, test_list_item):
    login_page = LoginPage(driver)
    login_page.login(test_list_item["username"], test_list_item["password"])
    assert login_page.get_error_message() == test_list_item["expected_error"], "Expected error message for invalid credentials not displayed"


# L7 — performance_glitch_user login (document expected delay, not a failure)
@pytest.mark.parametrize("test_list_item", [test_list[6]])
def test_performance_glitch_user_login(driver, test_list_item):
    # This user has valid credentials but the site adds an artificial delay
    # before redirecting to inventory. implicitly_wait(10) in conftest.py
    # covers it — no extra wait needed here.
    login_page = LoginPage(driver)
    login_page.login(test_list_item["username"], test_list_item["password"])
    assert InventoryPage(driver).is_loaded(), "Inventory page did not load for performance_glitch_user"
