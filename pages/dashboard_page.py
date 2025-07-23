import logging
import time

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

logger = logging.getLogger("test_logger")


class DashboardPage(BasePage):
    PAGE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
    WIDGET_LOCATOR = (By.XPATH, "//p[text()='{}']")

    def get_dashboard_page_url(self):
        return self.get_page_url()

    def is_widget_visible(self, widget_name):
        try:
            locator = (self.WIDGET_LOCATOR[0], self.WIDGET_LOCATOR[1].format(widget_name))
            element = self.wait_for_element(locator)
            return element.is_displayed()
        except TimeoutException as e:
            logger.error(f"Widget '{widget_name}' not found on the dashboard page - {str(e)}")
            return False
