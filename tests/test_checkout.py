from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


# CO1 — Complete checkout flow (happy path)
def test_complete_checkout_flow(driver, checkout_step_one):
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="John", last_name="Doe", postal_code="12345", submit=True)
    item_total, tax, total = checkout_page.get_summary_totals()
    assert item_total + tax == total, "Order total calculation is incorrect"
    checkout_page.finish()
    assert checkout_page.is_order_complete(), "Order complete page did not load after finishing checkout"

# CO2 — Missing first name
def test_missing_first_name(driver, checkout_step_one):
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="", last_name="Doe", postal_code="12345")
    assert checkout_page.get_error_message() == "Error: First Name is required", "Expected error message for missing first name not displayed"


# CO3 — Missing last name
def test_missing_last_name(driver, checkout_step_one):
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="John", last_name="", postal_code="12345")
    assert checkout_page.get_error_message() == "Error: Last Name is required", "Expected error message for missing last name not displayed"


# CO4 — Missing postal code
def test_missing_postal_code(driver, checkout_step_one):
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="John", last_name="Doe", postal_code="")
    assert checkout_page.get_error_message() == "Error: Postal Code is required", "Expected error message for missing postal code not displayed"


# CO5 — Cancel mid-checkout (cart state should be preserved)
def test_cancel_mid_checkout(driver, checkout_step_one):
    products = checkout_step_one
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="John", last_name="Doe", postal_code="12345", submit=False)
    checkout_page.cancel()
    cart_page = CartPage(driver)
    assert sorted(cart_page.get_item_names()) == sorted(products), "Cart items not preserved after cancelling mid-checkout"


# CO6 — Order total calculation (item prices + tax == displayed total)
def test_order_total_calculation(driver, checkout_step_one):
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="John", last_name="Doe", postal_code="12345", submit=True)
    item_total, tax, total = checkout_page.get_summary_totals()
    assert item_total + tax == total, "Order total calculation is incorrect"


# Bonus — cancelling from the overview step (after Continue) lands on the
# inventory page instead of the cart; cart contents should still be intact.
def test_cancel_order_after_calculation(driver, checkout_step_one):
    products = checkout_step_one
    checkout_page = CheckoutPage(driver)
    checkout_page.fill_info(first_name="John", last_name="Doe", postal_code="12345", submit=True)
    checkout_page.cancel()
    inventory_page = InventoryPage(driver)
    assert inventory_page.is_loaded()
    assert inventory_page.get_cart_count() == len(products)
    inventory_page.go_to_cart()
    cart_page = CartPage(driver)
    assert sorted(cart_page.get_item_names()) == sorted(products)
