import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    # Verified against saucedemo.com — double-check with DevTools if the site changes.
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_CLOSE_BUTTON = (By.CSS_SELECTOR, ".error-button")

    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        """Fills both fields and submits. Covers L1, L2, L6, L7 (matrix)."""
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        """Returns the error banner text. Covers L2, L3, L4, L5, L6."""
        error_el = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        )
        return error_el.text

    def close_error_message(self):
        """Clicks the X button to dismiss the error banner."""
        self.driver.find_element(*self.ERROR_CLOSE_BUTTON).click()

    def is_error_message_present(self):
        """Returns True if the error banner is still in the DOM."""
        return len(self.driver.find_elements(*self.ERROR_MESSAGE)) > 0

    def is_error_message_overflowing(self):
        """Checks whether the error text wraps to more lines than its
        container's fixed height allows — the extra line spills out and
        overlaps the Login button. Confirmed via DevTools: happens at
        viewport widths <= 443px and >= 900px, clean between 444-899px.
        Covers L8."""
        error_el = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        )
        container = error_el.find_element(By.XPATH, "./..")

        last_result = None
        for _ in range(5):
            current_result = self.driver.execute_script(
                "return arguments[0].scrollHeight > arguments[0].clientHeight;", container
            )
            if current_result == last_result:
                return current_result
            last_result = current_result
            time.sleep(0.1)

        return bool(last_result)
