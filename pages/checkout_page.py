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
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    # Confirmation step (third page)
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver

    def fill_info(self, first_name, last_name, postal_code):
        """Fills the checkout form. Passing an empty string leaves a field blank
        so the app can show the required-field validation error."""
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
                element.send_keys(value)

        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        ).click()

    def get_error_message(self):
        """Returns the validation error text shown when a required field is blank."""
        error = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        )
        return error.text

    def cancel(self):
        """Clicks the cancel button. Useful for the mid-checkout test."""
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.CANCEL_BUTTON)
        ).click()

    def get_summary_totals(self):
        """Returns (item_total, tax, total) as floats.
        Example text: 'Item total: $29.99' -> 29.99"""
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
        """Clicks the Finish button on the overview page."""
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.FINISH_BUTTON)
        ).click()

    def is_order_complete(self):
        """Returns True when the confirmation page is visible."""
        try:
            header = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.COMPLETE_HEADER)
            )
        except Exception:
            return False
        return "THANK YOU FOR YOUR ORDER" in header.text.upper()
