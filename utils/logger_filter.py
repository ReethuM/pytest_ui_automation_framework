import logging


class TestNameFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.test_name = ""

    def set_test_name(self, name):
        self.test_name = name

    def filter(self, record):
        record.test_name = self.test_name or "UNKNOWN"
        return True
