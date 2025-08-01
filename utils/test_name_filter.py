import logging

_current_test_name = None


def set_test_name(name):
    global _current_test_name
    _current_test_name = name


def get_test_name():
    return _current_test_name


class TestNameFilter(logging.Filter):
    def filter(self, record):
        record.test_name = _current_test_name
        return True
