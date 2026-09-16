from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    PAGE_TITLE = (By.CLASS_NAME, "title")
    EXPECTED_TITLE_TEXT = "Products"
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    INVENTORY_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    INVENTORY_ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    # SauceDemo uses a data-test attribute for each product button, like:
    # "add-to-cart-sauce-labs-backpack".
    # We can build the locator from the product slug instead of hard-coding
    # each product in the page object.

    def __init__(self, driver):
        self.driver = driver

    def is_loaded(self):
        """Confirms the user is on the Inventory page.
        We wait for the page title because the app can be slow on
        performance_glitch_user. Covers L1, L7."""
        try:
            title_el = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.PAGE_TITLE)
            )
        except TimeoutException:
            return False
        return title_el.text == self.EXPECTED_TITLE_TEXT

    def sort_by(self, option_text):
        """Chooses a sort option, such as 'Name (A to Z)'.
        The Select helper keeps the code simple and readable."""
        dropdown = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.SORT_DROPDOWN)
        )
        Select(dropdown).select_by_visible_text(option_text)

    def get_displayed_names(self):
        """Returns product names in the order shown on the page.
        This is useful for checking sort results, not just whether the dropdown changed."""
        products = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_all_elements_located(self.INVENTORY_ITEM_NAME)
        )
        return [product.text for product in products]

    def get_displayed_prices(self):
        """Returns the displayed prices as floats.
        Example: '$29.99' becomes 29.99."""
        products = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_all_elements_located(self.INVENTORY_ITEM_PRICE)
        )
        return [float(product.text.replace('$', '')) for product in products]

    def add_to_cart(self, product_name):
        """Clicks the Add to cart button for a product, given its visible
        name (e.g. 'Sauce Labs Backpack'). SauceDemo's data-test attributes
        are always the name lowercased with spaces turned into hyphens
        (e.g. 'add-to-cart-sauce-labs-backpack').

        Clicks via JS — see CartPage.remove_item's docstring for why
        (native clicks can silently no-op here when document.hasFocus() is
        False, e.g. on the slower GitHub Actions runners even though this
        click fires right after page load)."""
        slug = product_name.strip().lower().replace(" ", "-")
        selector = (By.CSS_SELECTOR, f'[data-test="add-to-cart-{slug}"]')
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(selector)
        )
        self.driver.execute_script("arguments[0].click();", button)

    def remove_from_cart(self, product_id):
        """Clicks the Remove button for a product already in the cart.
        This pattern is the same as add_to_cart, but the button's
        data-test value starts with 'remove-'.

        Clicks via JS — see CartPage.remove_item's docstring for why
        (native clicks can silently no-op here after a prior click/navigation)."""
        button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-test="remove-{product_id}"]'))
        )
        self.driver.execute_script("arguments[0].click();", button)

    def get_cart_count(self):
        """Returns the count shown in the cart badge.
        If the cart is empty, there is no badge, so we return 0."""
        badges = self.driver.find_elements(*self.CART_BADGE)
        if not badges:
            return 0
        return int(badges[0].text)

    def go_to_cart(self):
        """Clicks the cart icon and opens the cart page.

        Clicks via JS rather than a native WebDriver click — see
        CartPage.remove_item for why: a native click after another
        click/navigation on this site can silently no-op in headless
        Chrome when document.hasFocus() is False."""
        cart_link = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.CART_LINK)
        )
        self.driver.execute_script("arguments[0].click();", cart_link)
