from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    # Remove buttons follow the same pattern as Add to cart:
    # "remove-sauce-labs-backpack"

    def __init__(self, driver):
        self.driver = driver

    def get_item_names(self):
        """Returns the names of every product in the cart.
        If the cart is empty, it returns an empty list instead of failing."""
        items = self.driver.find_elements(*self.CART_ITEM_NAME)
        if not items:
            return []
        return [item.text for item in items]

    def remove_item(self, product_id):
        """Clicks the remove button for a product using its product ID.
        Example: 'sauce-labs-backpack' -> 'remove-sauce-labs-backpack'."""
        remove_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-test="remove-{product_id}"]'))
        )
        remove_button.click()

    def continue_shopping(self):
        """Clicks the 'Continue Shopping' button."""
        button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.CONTINUE_SHOPPING_BUTTON)
        )
        button.click()

    def go_to_checkout(self):
        """Clicks the 'Checkout' button."""
        button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
        )
        button.click()
