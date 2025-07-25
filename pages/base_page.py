import logging

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger("test_logger")


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.TIMEOUT = timeout

    def wait_for_element(self, locator):
        try:
            element = WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for element {locator}")
            raise

    def click(self, locator):
        self.wait_for_element(locator).click()

    def type(self, locator, text):
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.wait_for_element(locator).text

    def get_page_url(self):
        current_url = self.driver.current_url
        return current_url
