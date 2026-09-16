from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from tests.test_data_loader import VALID_USER


# CO1 — Complete checkout flow (happy path)
def test_complete_checkout_flow(driver):
    products = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    login_page = LoginPage(driver)
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    inventory_page = InventoryPage(driver)
    for product in products:
        inventory_page.add_to_cart(product)
    inventory_page.go_to_cart()
    cart_page = CartPage(driver)
    cart_page.go_to_checkout()


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
