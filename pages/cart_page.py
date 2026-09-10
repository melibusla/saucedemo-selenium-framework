from selenium.webdriver.common.by import By


class CartPage:
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    # Remove buttons follow the same data-test pattern as add-to-cart,
    # e.g. "remove-sauce-labs-backpack".

    def __init__(self, driver):
        self.driver = driver

    def get_item_names(self):
        """Covers C4 (confirming an item survived navigation)."""
        # TODO
        pass

    def remove_item(self, product_slug):
        """Covers C3."""
        # TODO
        pass

    def continue_shopping(self):
        # TODO
        pass

    def go_to_checkout(self):
        # TODO
        pass
