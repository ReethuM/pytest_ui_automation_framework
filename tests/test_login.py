import logging
import sys
import pytest

from helpers.user_login import perform_valid_login, perform_invalid_login
from pages.login_page import LoginPage

logger = logging.getLogger("test_logger")


@pytest.mark.login
@pytest.mark.usefixtures("driver")
class TestLogin:

    @pytest.mark.smoke
    @pytest.mark.skipif(sys.platform.startswith("linux"), reason="Not supported on Linux")
    def test_login_with_valid_credentials(self, driver, env_config):
        logger.info("User performing login with valid credentials.")
        perform_valid_login(driver, env_config["USERNAME"], env_config["PASSWORD"])

    @pytest.mark.negative
    @pytest.mark.parametrize("username, password", [
        ("Admin", "pass123"),  # wrong password
        ("", "abc123"),  # empty username
        ("Admin", "")  # empty password
    ])
    def test_login_with_invalid_credentials(self, driver, username, password):
        logger.info("Attempting login with invalid credentials.")
        message = perform_invalid_login(driver, username, password)
        assert message == "Invalid credentials", f"Expected error message not displayed, got: {message}"
        logger.info("Error message validated successfully for invalid login attempt")

    @pytest.mark.negative
    def test_login_with_empty_credentials(self, driver):
        """Verify login fails with both username and password empty"""
        logger.info("Attempting login with empty credentials.")
        perform_invalid_login(driver, "", "")
        logger.info("Login unsuccessful")

    @pytest.mark.positive
    def test_forgot_password(self, driver, env_config):
        """Verify forgot password functionality"""
        logger.info("Verifying forgot password functionality")
        login_page = LoginPage(driver)
        login_page.click_forgot_password_link()
        login_page.enter_username(env_config["USERNAME"])
        login_page.click_reset_password_button()
        assert login_page.is_password_reset_email_sent() == "Reset Password link sent successfully"
