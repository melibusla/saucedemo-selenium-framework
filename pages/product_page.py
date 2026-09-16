from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductPage:
    def __init__(self, driver):
        self.driver = driver

    def add_to_cart(self, product_id):
        """Clicks the add to cart button for a product using its product ID.
        Example: 'sauce-labs-backpack' -> 'add-to-cart-sauce-labs-backpack'.

        Clicks via JS — see CartPage.remove_item's docstring for why
        (native clicks can silently no-op here after a prior click/navigation)."""
        add_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-test="add-to-cart-{product_id}"]'))
        )
        self.driver.execute_script("arguments[0].click();", add_button)

    def remove_from_cart(self, product_id):
        """Clicks the remove button for a product using its product ID.
        Example: 'sauce-labs-backpack' -> 'remove-sauce-labs-backpack'.

        Clicks via JS — see CartPage.remove_item's docstring for why
        (native clicks can silently no-op here after a prior click/navigation)."""
        remove_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-test="remove-{product_id}"]'))
        )
        self.driver.execute_script("arguments[0].click();", remove_button)

    def back_to_products(self):
        """Clicks the 'Back to Products' button.

        Clicks via JS — see CartPage.remove_item's docstring for why
        (native clicks can silently no-op here after a prior click/navigation)."""
        back_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "back-to-products"))
        )
        self.driver.execute_script("arguments[0].click();", back_button)