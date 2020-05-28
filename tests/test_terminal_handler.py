import unittest
from src.exceptionite.errors.TerminalHandler import TerminalHandler

class TestTerminalHandler(unittest.TestCase):

    def test_outputs_handler(self):
        try:
            2 / 0
        except Exception as e:
            TerminalHandler(e).render()