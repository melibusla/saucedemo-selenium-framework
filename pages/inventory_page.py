from selenium.webdriver.common.by import By


class InventoryPage:
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    INVENTORY_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    INVENTORY_ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    # Add-to-cart buttons use a data-test attribute per product, e.g.
    # "add-to-cart-sauce-labs-backpack" — you'll need one locator per product
    # you actually test, or a helper that builds the locator from the product name.

    def __init__(self, driver):
        self.driver = driver

    def sort_by(self, option_text):
        """Selects a sort option (e.g. 'Name (A to Z)', 'Price (low to high)').
        Covers I1-I4."""
        # TODO
        pass

    def get_displayed_names(self):
        """Returns the list of product names in the order they're displayed.
        Use this to verify sort order, not just that a sort ran. Covers I1-I5."""
        # TODO
        pass

    def get_displayed_prices(self):
        """Returns the list of product prices as floats, in displayed order.
        Covers I3, I4."""
        # TODO
        pass

    def add_to_cart(self, product_slug):
        """product_slug matches SauceDemo's data-test suffix, e.g. 'sauce-labs-backpack'.
        Covers C1, C2."""
        # TODO
        pass

    def get_cart_count(self):
        """Reads the cart badge number. Returns 0 if the badge isn't present
        (empty cart shows no badge at all). Covers C1, C2, C4."""
        # TODO
        pass

    def go_to_cart(self):
        # TODO
        pass
