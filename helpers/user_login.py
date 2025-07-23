import logging

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

logger = logging.getLogger("test_logger")


def login(driver, username, password):
    """Perform login action and return the LoginPage object."""
    login_page = LoginPage(driver)
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login_button()
    return login_page


def perform_valid_login(driver, username, password):
    """Login with valid credentials and return Dashboard page object."""
    user_login = login(driver, username, password)
    assert user_login.is_logged_in(), "Login failed with valid credentials"
    logger.info("User is logged in successfully")
    return DashboardPage(driver)


def perform_invalid_login(driver, username, password):
    """Attempt login with invalid credentials and assert error is displayed."""
    try:
        user_login = login(driver, username, password)
        error_displayed = user_login.get_error_message()
        return error_displayed
    except Exception as e:
        logger.exception(f"Unexpected exception occurred during invalid login test: {e}")
        raise
