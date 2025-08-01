import logging
import logging.config
import os
from utils.test_name_filter import TestNameFilter


class LoggerSetup:
    @staticmethod
    def setup_logger():
        config_file = os.path.join(os.path.dirname(__file__), "logger.ini")
        logging.config.fileConfig(config_file, disable_existing_loggers=False)

        # Apply test name filter to all loggers we want
        for name in ["frameworkLogger", "selenium", "urllib3"]:
            logger = logging.getLogger(name)
            for handler in logger.handlers:
                handler.addFilter(TestNameFilter())

        # Return only the main logger for tests
        return logging.getLogger("frameworkLogger")
