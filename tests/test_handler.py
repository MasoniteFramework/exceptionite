import unittest

from src.exceptionite import Handler


class TestHandler(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.handler = Handler()

    def test_handler_can_provide_basic_exception_data(self):
        try:
            raise ValueError("Custom message")
        except Exception as exception:
            self.handler.start(exception)

        assert self.handler.message() == "Custom message"
        assert self.handler.exception() == "ValueError"
        assert self.handler.namespace() == "builtins.ValueError"
        assert self.handler.count() > 0

        frame = self.handler.stacktrace()[0]
        assert frame.index == 0
        assert frame.relative_file == "tests/test_handler.py"
        assert not frame.is_vendor
        assert frame.lineno == 13
        assert frame.offending_line == 13
        assert frame.method == "test_handler_can_provide_basic_exception_data"
