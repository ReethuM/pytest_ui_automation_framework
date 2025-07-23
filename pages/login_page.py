import logging

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage

logger = logging.getLogger("test_logger")


class LoginPage(BasePage):
    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    INVALID_CREDENTIALS = (By.XPATH, "//p[text()='Invalid credentials']")
    HOME_PAGE_TEXT = (By.XPATH, "//p[text()='Time at Work']")

    def enter_username(self, username):
        logger.info("Entering username")
        self.type(self.USERNAME_FIELD, username)

    def enter_password(self, password):
        logger.info("Entering password")
        self.type(self.PASSWORD_FIELD, password)

    def click_login_button(self):
        logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        message = self.get_text(self.INVALID_CREDENTIALS)
        return message

    def is_logged_in(self):
        try:
            self.wait_for_element(self.HOME_PAGE_TEXT)
            return True
        except TimeoutException as e:
            logger.error(f"Login check failed: {e}")
            return False
