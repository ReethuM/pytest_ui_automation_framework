import logging
import os
import pytest

from selenium import webdriver
from pytest_html import extras

from helpers.user_login import perform_valid_login
from utils.config_loader import load_config
from utils.logger_filter import TestNameFilter
from utils.screenshot_utils import take_screenshot

test_name_filter = TestNameFilter()
logger = logging.getLogger("test_logger")


@pytest.fixture(scope="session")
def env_config():
    return load_config()


@pytest.fixture(params=["chrome", "edge"])
def driver(request, env_config):
    logger.info("------ Starting browser session ------")
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "edge":
        driver = webdriver.Edge()
    else:
        pytest.skip(f"Unsupported browser: {request.param}")
        return

    logger.info(f"Navigating to: {env_config['BASE_URL']}")
    driver.get(env_config['BASE_URL'])
    driver.maximize_window()
    yield driver
    logger.info("------ Closing browser session ------")
    driver.quit()


@pytest.fixture
def dashboard_page(driver, env_config):
    return perform_valid_login(driver, env_config["USERNAME"], env_config["PASSWORD"])


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

    # logs from selenium and urllib3
    sel_handler = logging.FileHandler("logs/selenium.log", mode="w")
    sel_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s"))

    for name in ["selenium", "urllib3"]:
        sel_urllib3_logger = logging.getLogger(name)
        sel_urllib3_logger.setLevel(logging.WARNING)
        sel_urllib3_logger.addHandler(sel_handler)
        sel_urllib3_logger.propagate = False


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
