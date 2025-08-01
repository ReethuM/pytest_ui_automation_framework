import os
import pytest
from datetime import datetime
from selenium import webdriver
from pytest_html import extras

from helpers.user_login import UserLoginHelper
from utils.config.config_loader import ConfigLoader
from utils.test_name_filter import set_test_name
from utils.screenshot_utils import ScreenshotManager
from utils.logger.logger import LoggerSetup

logger = LoggerSetup.setup_logger()


@pytest.fixture(scope="session")
def env_config():
    return ConfigLoader.load_config()


@pytest.fixture(params=["chrome", "edge"])
def driver(request, env_config):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "edge":
        driver = webdriver.Edge()
    else:
        pytest.skip(f"Unsupported browser: {request.param}")
        return
    logger.info("------ Starting browser session ------")
    logger.info(f"Navigating to: {env_config['BASE_URL']}")
    driver.get(env_config['BASE_URL'])
    driver.maximize_window()
    yield driver
    logger.info("------ Closing browser session ------")
    driver.quit()


@pytest.fixture
def dashboard_page(driver, env_config):
    return UserLoginHelper.perform_valid_login(driver, env_config["USERNAME"], env_config["PASSWORD"])


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_setup(item):
    """ Hook to set test name before each test """
    set_test_name(item.name)
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # Attach screenshot if test failed
    if report.when == "call":
        driver = item.funcargs.get("driver", None)
        if driver:
            test_name = item.name
            status = "failed" if report.failed else "passed"
            screenshot_path = ScreenshotManager.take_screenshot(driver, test_name, status)
            extra = getattr(report, "extra", [])
            if report.failed and screenshot_path:
                print(f"Screenshotpath: {screenshot_path}")
                extra.append(extras.image(screenshot_path))
            report.extra = extra


def pytest_configure(config):
    """Dynamically set report path with test name and timestamp"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H-%M-%S")

    reports_dir = os.path.join("reports", date_str)
    os.makedirs(reports_dir, exist_ok=True)

    report_file = f"test_report_{time_str}.html"
    report_path = os.path.join(reports_dir, report_file)

    config.option.htmlpath = report_path
