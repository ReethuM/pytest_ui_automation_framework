from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger.logger import LoggerSetup


# Implement base page at framework level, consider creating classes like base_page_wait, etc..
class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.TIMEOUT = timeout
        self.logger = LoggerSetup.setup_logger()

    def wait_for_element(self, locator):
        try:
            element = WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element {locator}")
            raise

    def click(self, locator):
        try:
            element = WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except ElementNotInteractableException:
            self.logger.error(f"Element not interactable: {locator}")
            raise

    def type(self, locator, text):
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.wait_for_element(locator).text

    def get_page_url(self):
        page_url = self.driver.current_url
        return page_url
