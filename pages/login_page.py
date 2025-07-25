import logging

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage

logger = logging.getLogger("test_logger")


class LoginPage(BasePage):
    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    INVALID_CREDENTIALS = (By.XPATH, "//p[text()='Invalid credentials']")
    HOME_PAGE_TEXT = (By.XPATH, "//p[text()='Time at Work']")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//p[text()='Forgot your password? ']")
    RESET_PASSWORD = (By.XPATH, "//button[text()=' Reset Password ']")
    PASSWORD_RESET_MESSAGE = (By.XPATH, "//div/h6[text()='Reset Password link sent successfully']")

    def enter_username(self, username):
        logger.info("User is entering the username")
        self.type(self.USERNAME_FIELD, username)

    def enter_password(self, password):
        logger.info("User is entering the password")
        self.type(self.PASSWORD_FIELD, password)

    def click_login_button(self):
        logger.info("User clicks on the login button")
        self.click(self.LOGIN_BUTTON)

    def click_forgot_password_link(self):
        logger.info("User clicks on Forgot Password link")
        self.click(self.FORGOT_PASSWORD_LINK)

    def click_reset_password_button(self):
        logger.info("User clicks on Reset password")
        self.click(self.RESET_PASSWORD)

    def get_error_message(self):
        message = self.get_text(self.INVALID_CREDENTIALS)
        return message

    def is_logged_in(self):
        try:
            self.wait_for_element(self.HOME_PAGE_TEXT)
            return True
        except Exception as e:
            logger.error(f"User login failed: {e}")
            return False

    def is_password_reset_email_sent(self):
        try:
            message = self.get_text(self.PASSWORD_RESET_MESSAGE)
            logger.info("Reset password link has been sent to the user via email")
            return message
        except TimeoutException:
            logger.error(f"Password reset email confirmation is not displayed")
            raise
