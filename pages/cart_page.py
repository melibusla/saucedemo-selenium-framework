from selenium.common.exceptions import StaleElementReferenceException
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
        for _ in range(3):
            try:
                items = self.driver.find_elements(*self.CART_ITEM_NAME)
                return [item.text for item in items]
            except StaleElementReferenceException:
                continue
        return []

    def remove_item(self, product_id):
        """Clicks the remove button for a product using its product ID.
        Example: 'sauce-labs-backpack' -> 'remove-sauce-labs-backpack'.

        Ignores StaleElementReferenceException while polling: the cart page
        re-renders shortly after load, which can make element_to_be_clickable
        grab a node right before it gets swapped out (see get_item_names,
        which hits the same issue).

        Clicks via JS instead of a native WebDriver click: in headless
        Chrome, document.hasFocus() can be False right after navigating to
        this page (e.g. via InventoryPage.go_to_cart()), and a native click
        silently no-ops when that happens (no exception, button just stays
        put). Dispatching element.click() directly through the DOM sidesteps
        the focus-dependent synthetic mouse event."""
        remove_button = WebDriverWait(
            self.driver, 5, ignored_exceptions=(StaleElementReferenceException,)
        ).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-test="remove-{product_id}"]'))
        )
        self.driver.execute_script("arguments[0].click();", remove_button)

    def continue_shopping(self):
        """Clicks the 'Continue Shopping' button.

        Clicks via JS — see remove_item's docstring for why (native clicks
        can silently no-op here after a prior click/navigation)."""
        button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.CONTINUE_SHOPPING_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)

    def go_to_checkout(self):
        """Clicks the 'Checkout' button."""
        button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)

    def click_item(self, product_name):
        """Clicks the name of a product in the cart to go to its details page."""
        for _ in range(3):
            try:
                items = self.driver.find_elements(*self.CART_ITEM)
                for item in items:
                    name_el = item.find_element(*self.CART_ITEM_NAME)
                    if name_el.text.strip() == product_name:
                        self.driver.execute_script("arguments[0].click();", name_el)
                        return
                raise ValueError(f"Product '{product_name}' not found in cart.")
            except StaleElementReferenceException:
                continue
        raise RuntimeError("Failed to click item due to repeated stale element references.")
