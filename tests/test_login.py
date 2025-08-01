import sys
import pytest

from helpers.user_login import UserLoginHelper
from pages.login_page import LoginPage


@pytest.mark.login
class TestLogin:

    @pytest.mark.smoke
    @pytest.mark.skipif(sys.platform.startswith("linux"), reason="Not supported on Linux")
    def test_login_with_valid_credentials(self, driver, env_config):
        UserLoginHelper.perform_valid_login(driver, env_config["USERNAME"], env_config["PASSWORD"])

    @pytest.mark.negative
    @pytest.mark.parametrize("username, password", [
        ("Admin", "pass123"),  # wrong password
        ("", "abc123"),  # empty username
        ("Admin", "")  # empty password
    ])
    def test_login_with_invalid_credentials(self, driver, username, password):
        message = UserLoginHelper.perform_invalid_login(driver, username, password)
        assert message == "Invalid credentials", f"Expected error message not displayed, got: {message}"

    @pytest.mark.negative
    def test_login_with_empty_credentials(self, driver):
        """Verify login fails with both username and password empty"""
        UserLoginHelper.perform_invalid_login(driver, "", "")

    @pytest.mark.positive
    def test_forgot_password(self, driver, env_config):
        """Verify forgot password functionality"""
        login_page = LoginPage(driver)
        login_page.click_forgot_password_link()
        login_page.enter_username(env_config["USERNAME"])
        login_page.click_reset_password_button()
        assert login_page.is_password_reset_email_sent() == "Reset Password link sent successfully"
