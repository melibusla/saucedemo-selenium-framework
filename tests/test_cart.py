from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.product_page import ProductPage
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
    products = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    login_page = LoginPage(driver)
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    inventory_page = InventoryPage(driver)
    for product in products:
        inventory_page.add_to_cart(product)
    cart_count = inventory_page.get_cart_count()
    assert cart_count == len(products)
    inventory_page.go_to_cart()
    cart_page = CartPage(driver)
    assert sorted(cart_page.get_item_names()) == sorted(products)


# C3 — Remove item from cart
def test_remove_item_while_in_inventory(driver):
    login_page = LoginPage(driver)
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    inventory_page = InventoryPage(driver)
    inventory_page.add_to_cart("Sauce Labs Backpack")
    cart_count = inventory_page.get_cart_count()
    assert cart_count == 1
    inventory_page.remove_from_cart("sauce-labs-backpack")
    cart_count = inventory_page.get_cart_count()
    assert cart_count == 0


# C4 — Cart persists across navigation
def test_cart_persists_across_navigation(driver):
    products = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    login_page = LoginPage(driver)
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    inventory_page = InventoryPage(driver)
    for product in products:
        inventory_page.add_to_cart(product)
    cart_count = inventory_page.get_cart_count()
    assert cart_count == len(products)
    inventory_page.go_to_cart()
    cart_page = CartPage(driver)
    assert sorted(cart_page.get_item_names()) == sorted(products)
    cart_page.continue_shopping()
    assert inventory_page.get_cart_count() == len(products)
    inventory_page.go_to_cart()
    assert sorted(cart_page.get_item_names()) == sorted(products)
    cart_page.click_item("Sauce Labs Backpack")
    assert inventory_page.get_cart_count() == len(products)
    product_page = ProductPage(driver)
    product_page.back_to_products()
    assert inventory_page.get_cart_count() == len(products)
    inventory_page.go_to_cart()
    assert sorted(cart_page.get_item_names()) == sorted(products)

def test_remove_item_from_cart(driver):
    products = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    login_page = LoginPage(driver)
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    inventory_page = InventoryPage(driver)
    for product in products:
        inventory_page.add_to_cart(product)
    inventory_page.go_to_cart()
    cart_page = CartPage(driver)
    cart_page.remove_item("sauce-labs-backpack")
    assert cart_page.get_item_names() == ["Sauce Labs Bike Light"]
