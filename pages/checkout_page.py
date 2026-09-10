from selenium.webdriver.common.by import By


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
        """Fills step-one form. Leave a field as '' to trigger its validation
        error. Covers CO1, CO2, CO3, CO4."""
        # TODO
        pass

    def get_error_message(self):
        """Covers CO2, CO3, CO4."""
        # TODO
        pass

    def cancel(self):
        """Covers CO5 — check the cart afterwards to confirm it wasn't cleared."""
        # TODO
        pass

    def get_summary_totals(self):
        """Returns (item_total, tax, total) as floats, to verify the math
        yourself rather than trusting the displayed total. Covers CO6."""
        # TODO
        pass

    def finish(self):
        """Covers CO1."""
        # TODO
        pass

    def is_order_complete(self):
        """Covers CO1."""
        # TODO
        pass
