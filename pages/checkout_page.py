from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Overview step (second page of checkout)
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    # Confirmation step (third page)
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    GENERATE_PDF_BUTTON = (By.ID, "generate-pdf-order")

    def __init__(self, driver):
        self.driver = driver

    def fill_info(self, first_name, last_name, postal_code, submit=True):
        """Fills the checkout form. Passing an empty string leaves a field blank
        so the app can show the required-field validation error.

        submit=False fills the fields but doesn't click Continue, leaving the
        page on checkout-step-one. This matters for cancel(): the Cancel
        button behaves differently depending on step — step one returns to
        the cart, step two (after Continue) returns to the inventory page
        instead. See test_cancel_mid_checkout.

        The Continue click is dispatched via JS — see CartPage.remove_item's
        docstring for why (native clicks can silently no-op here when
        document.hasFocus() is False, which this hit on GitHub Actions
        runners after filling three fields even though it didn't locally)."""
        fields = [
            (self.FIRST_NAME_INPUT, first_name),
            (self.LAST_NAME_INPUT, last_name),
            (self.POSTAL_CODE_INPUT, postal_code),
        ]

        for locator, value in fields:
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator)
            )
            element.clear()
            if value:
                # Same headless-Chrome "document.hasFocus() is False" quirk
                # as the JS-click fix (see CartPage.remove_item's docstring)
                # can also swallow send_keys()'s implicit focus/keystrokes —
                # on CI this showed up as fields silently staying empty
                # (e.g. the app reporting "First Name is required" right
                # after typing "John" into it). Forcing focus via JS first
                # sidesteps the same focus dependency.
                self.driver.execute_script("arguments[0].focus();", element)
                element.send_keys(value)
                try:
                    WebDriverWait(self.driver, 5).until(
                        lambda d, locator=locator, value=value: d.find_element(*locator).get_attribute("value") == value
                    )
                except Exception:
                    actual = self.driver.find_element(*locator).get_attribute("value")
                    has_focus = self.driver.execute_script("return document.hasFocus();")
                    active_id = self.driver.execute_script("return document.activeElement && document.activeElement.id;")
                    print(f"DEBUG fill_info mismatch: locator={locator} expected={value!r} actual={actual!r} hasFocus={has_focus} activeElementId={active_id!r} url={self.driver.current_url}")
                    raise

        if submit:
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CONTINUE_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", button)

    def get_error_message(self):
        """Returns the validation error text shown when a required field is blank."""
        error = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        )
        return error.text

    def cancel(self):
        """Clicks the cancel button. Useful for the mid-checkout test.

        Clicks via JS — see CartPage.remove_item's docstring for why
        (native clicks can silently no-op here after a prior click/navigation)."""
        button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.CANCEL_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)

    def get_line_items(self):
        """Returns [(name, price_text), ...] for each product on the
        overview page. Reuses the same 'inventory_item_name' /
        'inventory_item_price' classes as the inventory and cart pages —
        confirmed by inspection that SauceDemo renders this list with the
        same components, in the same order (name[i] pairs with price[i])."""
        names = self.driver.find_elements(*self.ITEM_NAME)
        prices = self.driver.find_elements(*self.ITEM_PRICE)
        return list(zip((n.text for n in names), (p.text for p in prices)))

    def get_summary_totals(self):
        """Returns (item_total, tax, total) as floats.
        Example text: 'Item total: $29.99' -> 29.99"""
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.TOTAL_LABEL)
        )
        item_total = self.driver.find_element(*self.ITEM_TOTAL).text
        tax = self.driver.find_element(*self.TAX_LABEL).text
        total = self.driver.find_element(*self.TOTAL_LABEL).text

        def parse_money(label_text):
            # Remove the text before the dollar sign and then convert to float.
            return float(label_text.split('$')[-1])

        return (
            parse_money(item_total),
            parse_money(tax),
            parse_money(total),
        )

    def finish(self):
        """Clicks the Finish button on the overview page.

        Clicks via JS — see CartPage.remove_item's docstring for why (native
        clicks can silently no-op here right after a prior click, and this
        one fires immediately after fill_info's Continue click)."""
        button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.FINISH_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)

    def is_order_complete(self):
        """Returns True when the confirmation page is visible."""
        try:
            header = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.COMPLETE_HEADER)
            )
        except Exception:
            return False
        return "THANK YOU FOR YOUR ORDER" in header.text.upper()

    def back_home(self):
        """Clicks 'Back Home' on the order confirmation page, returning to
        the inventory page. Shares its id ('back-to-products') with
        ProductPage.back_to_products — SauceDemo reuses the same button id
        across pages — but this is the confirmation page's button.

        Clicks via JS — see CartPage.remove_item's docstring for why
        (native clicks can silently no-op here after a prior click/navigation)."""
        button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.BACK_HOME_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)

    def generate_pdf_order(self):
        """Clicks 'Generate PDF order' on the confirmation page, which
        triggers a browser file download. The click alone doesn't confirm
        the file arrived — see test_generate_pdf_order for how the download
        itself is verified.

        Clicks via JS — see CartPage.remove_item's docstring for why
        (native clicks can silently no-op here after a prior click/navigation)."""
        button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.GENERATE_PDF_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)
