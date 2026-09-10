from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


# CO1 — Complete checkout flow (happy path)
def test_complete_checkout_flow(driver):
    pass


# CO2 — Missing first name
def test_missing_first_name(driver):
    pass


# CO3 — Missing last name
def test_missing_last_name(driver):
    pass


# CO4 — Missing postal code
def test_missing_postal_code(driver):
    pass


# CO5 — Cancel mid-checkout (cart state should be preserved)
def test_cancel_mid_checkout(driver):
    pass


# CO6 — Order total calculation (item prices + tax == displayed total)
def test_order_total_calculation(driver):
    pass
