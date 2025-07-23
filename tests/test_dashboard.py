import logging

import pytest

logger = logging.getLogger("test_logger")


@pytest.mark.ui
class TestDashboard:

    def test_validate_page_url(self, dashboard_page):
        assert dashboard_page.get_dashboard_page_url() == dashboard_page.PAGE_URL
        logger.info("Dashboard page URL verified successfully")

    @pytest.mark.parametrize("widget_name", ["Time at Work", "My Actions", "Employees on Leave Today"])
    def test_dashboard_widget_visibility(self, dashboard_page, widget_name):
        """Check if the specified dashboard widgets are visible."""
        assert dashboard_page.is_widget_visible(widget_name)
        logger.info(f"Dashboard page contains widget: {widget_name}")

    @pytest.mark.xfail(reason="Widget 'My Plans' not available on dashboard yet")
    def test_is_my_plans_widget_visible(self, dashboard_page):
        """Verify that the 'My Plans' widget is not visible on the dashboard."""
        assert dashboard_page.is_widget_visible("My Plans")
