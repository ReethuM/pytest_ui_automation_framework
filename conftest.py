import logging
import os
import pytest

from selenium import webdriver
from pytest_html import extras

from helpers.user_login import perform_valid_login
from pages.dashboard_page import DashboardPage
from utils.config_loader import load_config
from utils.logger_filter import TestNameFilter
from utils.screenshot_utils import take_screenshot

test_name_filter = TestNameFilter()


@pytest.fixture(scope="session")
def config():
    return load_config()


@pytest.fixture(params=["chrome", "edge"])
def browser(request):
    return request.param


@pytest.fixture
def driver(browser, config):
    if browser == "chrome":
        driver = webdriver.Chrome()
    # elif browser == "edge":
    #     driver = webdriver.Edge()
    else:
        pytest.skip(f"Unsupported browser: {browser}")
        return

    driver.get(config['BASE_URL'])
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def dashboard_page(driver, config):
    return perform_valid_login(driver, config["USERNAME"], config["PASSWORD"])


@pytest.fixture(scope="session", autouse=True)
def configure_logging(worker_id):
    os.makedirs("logs", exist_ok=True)

    # Creating custom logger
    test_logger = logging.getLogger()
    test_logger.setLevel(logging.INFO)

    # File handler
    log_file = f"logs/{worker_id}.log"
    file_handler = logging.FileHandler(log_file, mode='w')
    file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(test_name)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    file_handler.addFilter(test_name_filter)

    test_logger.addHandler(file_handler)

    # logs from selenium
    selenium_logger = logging.getLogger("selenium")
    selenium_logger.setLevel(logging.INFO)

    selenium_log_file = logging.FileHandler("logs/selenium.log", mode="w")
    selenium_log_format = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
    selenium_log_file.setFormatter(selenium_log_format)

    selenium_logger.addHandler(selenium_log_file)

    # logs for urllib3
    urllib3_logger = logging.getLogger("urllib3")
    urllib3_logger.setLevel(logging.WARNING)
    urllib3_logger.addHandler(selenium_log_file)


# Hook to set test name before each test
def pytest_runtest_setup(item):
    test_name_filter.set_test_name(item.name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # Attach screenshot if test failed
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot_path = take_screenshot(driver, item.name)
            if screenshot_path:
                # Attach screenshot to report
                extra = getattr(report, "extra", [])
                extra.append(extras.image(screenshot_path))
                report.extras = extra
