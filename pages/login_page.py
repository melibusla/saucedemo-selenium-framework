from selenium.webdriver.common.by import By


class LoginPage:
    # Verified against saucedemo.com — double-check with DevTools if the site changes.
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        """Fills both fields and submits. Covers L1, L2, L6, L7 (matrix)."""
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        """Returns the error banner text. Covers L2, L3, L4, L5, L6."""
        errormessage = self.driver.find_element(*self.ERROR_MESSAGE).text
        return errormessage
