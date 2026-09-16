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

    # Extra: the error banner's close button should dismiss it.
    login_page.close_error_message()
    assert not login_page.is_error_message_present(), "Error banner still present after clicking close"


# L7 — performance_glitch_user login (document expected delay, not a failure)
@pytest.mark.parametrize("test_list_item", [test_list[6]])
def test_performance_glitch_user_login(driver, test_list_item):
    # This user has valid credentials but the site adds an artificial delay
    # before redirecting to inventory. InventoryPage.is_loaded() has its own
    # WebDriverWait(10) that covers it — no extra wait needed here.
    login_page = LoginPage(driver)
    login_page.login(test_list_item["username"], test_list_item["password"])
    assert InventoryPage(driver).is_loaded(), "Inventory page did not load for performance_glitch_user"


# L8 — Error message overflow at certain viewport widths (bug found manually,
# confirmed with DevTools: the error text wraps to 3 lines and the extra line
# spills past its fixed-height container at these widths). Uses the L6
# credentials since that message is long enough to reproduce the wrap.
@pytest.mark.parametrize("width,expect_overflow", [(400, True), (700, False), (950, True)])
def test_error_message_overflow_at_viewport_widths(driver, request, width, expect_overflow):
    # CDP viewport emulation (see below) is Chrome-specific — Firefox has no
    # equivalent, so this test only runs when Chrome is the active browser.
    if request.config.getoption("browser_name") != "chrome":
        pytest.skip(
            "Emulation.setDeviceMetricsOverride is a Chrome DevTools Protocol "
            "command; no Firefox equivalent is used here."
        )
    # Emulate the viewport width directly via Chrome DevTools Protocol instead
    # of resizing the actual browser window. This avoids two OS-dependent
    # problems: window manager quirks that can block resizing after
    # maximize_window(), and the gap between requested window size and real
    # innerWidth caused by window chrome (borders/title bar), which differs
    # between Windows and Linux CI runners.
    driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "width": width,
        "height": 800,
        "deviceScaleFactor": 1,
        "mobile": False,
    })
    login_page = LoginPage(driver)
    login_page.login(test_list[5]["username"], test_list[5]["password"])
    assert login_page.is_error_message_overflowing() == expect_overflow, (
        f"Unexpected overflow state at viewport width={width}"
    )
