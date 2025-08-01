"""This module contains the BasePage class"""

from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger.logger import LoggerSetup


class BasePage:
    """Base class for all pages. Contains common utilities."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.logger = LoggerSetup.setup_logger()

    def wait_for_element(self, locator):
        """Wait for the given element to be present on the page."""
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            self.logger.error("Timeout waiting for element %s", locator)
            raise

    def click(self, locator):
        """Click on the button on a web page."""
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except ElementNotInteractableException:
            self.logger.error("Element %s not interactable", locator)
            raise

    def type(self, locator, text):
        """Typing text to the input field."""
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Return the text displayed on the page."""
        return self.wait_for_element(locator).text

    def get_page_url(self):
        """Return the current page URL from the browser."""
        page_url = self.driver.current_url
        return page_url
