"""This module contains the DashboardPage class"""
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Class containing the locators and actions of dashboard page."""
    PAGE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
    WIDGET_LOCATOR = (By.XPATH, "//p[text()='{}']")

    def get_dashboard_page_url(self):
        """To get the dashboard page url"""
        return self.get_page_url()

    def is_widget_visible(self, widget_name):
        """Return boolean value based of widget visibility on dashboard page"""
        try:
            locator = (self.WIDGET_LOCATOR[0], self.WIDGET_LOCATOR[1].format(widget_name))
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            self.logger.error("Widget %s not found on the dashboard page", widget_name)
            raise
