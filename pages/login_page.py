"""This module contains the LoginPage class"""
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Class containing the locators and actions of login page."""
    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    INVALID_CREDENTIALS = (By.XPATH, "//p[text()='Invalid credentials']")
    HOME_PAGE_TEXT = (By.XPATH, "//p[text()='Time at Work']")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//p[text()='Forgot your password? ']")
    RESET_PASSWORD = (By.XPATH, "//button[text()=' Reset Password ']")
    PASSWORD_RESET_MESSAGE = (By.XPATH, "//div/h6[text()='Reset Password link sent successfully']")

    def enter_username(self, username):
        """Enter the given username into the username input field."""
        self.logger.info("User is entering the username")
        self.type(self.USERNAME_FIELD, username)

    def enter_password(self, password):
        """Enter the given password into the password input field."""
        self.logger.info("User is entering the password")
        self.type(self.PASSWORD_FIELD, password)

    def click_login_button(self):
        """Clicking on login button."""
        self.logger.info("User clicks on the login button")
        self.click(self.LOGIN_BUTTON)

    def click_forgot_password_link(self):
        """Clicking on forgot password link."""
        self.logger.info("User clicks on Forgot Password link")
        self.click(self.FORGOT_PASSWORD_LINK)

    def click_reset_password_button(self):
        """Clicking on reset password button."""
        self.logger.info("User clicks on Reset password")
        self.click(self.RESET_PASSWORD)

    def get_error_message(self):
        """Return the error message displayed on the page."""
        message = self.get_text(self.INVALID_CREDENTIALS)
        return message

    def is_logged_in(self):
        """Return boolean value based on user logged ib status."""
        try:
            self.wait_for_element(self.HOME_PAGE_TEXT)
            return True
        except NoSuchElementException as e:
            self.logger.error("User login failed %s", e)
            return False

    def is_password_reset_email_sent(self):
        """Return message after password reset."""
        try:
            message = self.get_text(self.PASSWORD_RESET_MESSAGE)
            self.logger.info("Reset password link has been sent to the user via email")
            return message
        except TimeoutException:
            self.logger.error("Password reset email confirmation is not displayed")
            raise
