from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from tests.test_data_loader import VALID_USER


# C1 — Add single item to cart
def test_add_single_item(driver):
    login_page = LoginPage(driver)
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    inventory_page = InventoryPage(driver)
    inventory_page.add_to_cart("Sauce Labs Backpack")
    cart_count = inventory_page.get_cart_count()
    assert cart_count == 1
    inventory_page.go_to_cart()
    cart_page = CartPage(driver)
    product = cart_page.get_item_names()
    assert product[0] == "Sauce Labs Backpack"

# C2 — Add multiple items
def test_add_multiple_items(driver):
    pass


# C3 — Remove item from cart
def test_remove_item(driver):
    pass


# C4 — Cart persists across navigation
def test_cart_persists_across_navigation(driver):
    pass
