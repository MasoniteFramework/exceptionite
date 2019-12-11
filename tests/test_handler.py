from masonite.testing import TestCase
from src.masonite.errors import Handler


class TestPackage(TestCase):

    def setUp(self):
        super().setUp()

    def test_returns_error_message(self):
        try:
            2/0
        except Exception as e:
            handler = Handler(e)

        self.assertEqual(handler.message(), 'division by zero')
        self.assertEqual(handler.exception(), 'ZeroDivisionError')

    def test_returns_true_when_has_exception(self):
        try:
            2/0
        except Exception as e:
            handler = Handler(e)

        self.assertTrue(handler.any())

    def test_returns_correct_exception_count_trace(self):
        try:
            2/0
        except Exception as e:
            handler = Handler(e)

        self.assertEqual(handler.count(), 1)
