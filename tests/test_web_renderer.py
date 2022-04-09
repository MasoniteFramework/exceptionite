import unittest
from dotty_dict import dotty

from src.exceptionite import Handler, Tab


class CustomTestTab(Tab):
    id = "test"
    name = "Test tab"

    def build(self):
        return {"key": "value"}


class TestWebRenderer(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.handler = Handler()
        try:
            raise ValueError("Custom message")
        except Exception as exception:
            self.handler.start(exception)

    def test_enabled_tabs(self):
        web = self.handler.renderer("web")
        assert len(web.enabled_tabs()) == 3

    def test_build_page_context(self):
        context = dotty(self.handler.renderer("web").build())
        assert context.get("exception.type") == "ValueError"
        assert context.get("exception.namespace") == "builtins.ValueError"
        assert context.get("exception.message") == "Custom message"
        assert context.get("config")
        assert context.get("actions") == []
        context_tab = context.get("tabs")[0]
        assert context_tab.get("id") == "context"
        assert context_tab.get("name") == "Context"
        assert context_tab.get("has_content")
        assert not context_tab.get("has_sections")
        blocks = context_tab.get("blocks")
        assert len(blocks) == 3
        env_block = blocks[0]
        assert env_block.get("id") == "environment"
        assert env_block.get("name") == "System Environment"
        assert env_block.get("has_content")
        assert env_block.get("icon") == "TerminalIcon"
        assert env_block.get("data").get("Arch") == "64bit"

    def test_add_tabs(self):
        web = self.handler.renderer("web")
        web.add_tabs(CustomTestTab)
        assert len(web.enabled_tabs()) == 4

    def test_add_actions(self):
        pass

    def test_can_display_error_page(self):
        exception = ValueError("Custom message")
        self.handler.start(exception)

        assert "Custom message" in self.handler.render("web")
        assert "ValueError" in self.handler.render("web")
