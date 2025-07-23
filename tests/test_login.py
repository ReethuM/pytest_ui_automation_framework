import logging
import sys
import pytest

from helpers.user_login import perform_valid_login, perform_invalid_login

logger = logging.getLogger("test_logger")


class TestLogin:

    @pytest.mark.smoke
    @pytest.mark.skipif(sys.platform.startswith("linux"), reason="Not supported on Linux")
    def test_login_with_valid_credentials(self, driver, config):
        perform_valid_login(driver, config["USERNAME"], config["PASSWORD"])

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

    # @pytest.mark.negative
    def test_login_with_empty_credentials(self, driver):
        """Verify login fails with both username and password empty"""
        logger.info("Attempting login with empty credentials.")
        perform_invalid_login(driver, "", "")
        logger.info("Login unsuccessful")