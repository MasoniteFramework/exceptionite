from collections import OrderedDict
import os
from jinja2 import Environment, PackageLoader
from typing import Type, TYPE_CHECKING, List, Callable


if TYPE_CHECKING:
    from ..Tab import Tab
    from ..Handler import Handler
    from ..Action import Action

from ..tabs import ContextTab, SolutionsTab, RecommendationsTab
from ..exceptions import ConfigurationException, TabNotFound
from ..Block import Block


class WebRenderer:
    """Renderer used to render exception as a beautiful extendable HTML error page which ease
    debugging."""

    reserved_tabs = ["context"]

    def __init__(self, handler: "Handler") -> None:
        self.handler = handler
        # error page interface options
        self.tabs: dict = OrderedDict()
        self.actions: dict = {}
        self.context: dict = {}
        # setup base interface
        self.add_tabs(ContextTab, SolutionsTab, RecommendationsTab)

    def build(self) -> dict:
        """Build the handled exception context to inject into the error page."""
        from .. import __version__

        enabled_tabs = self.enabled_tabs()
        return {
            "config": {
                **self.handler.options.to_dict(),
                "absolute_path": os.getcwd(),
                "version": __version__,
            },
            "exception": {
                "type": self.handler.exception(),
                "message": self.handler.message(),
                "namespace": self.handler.namespace(),
                "stacktrace": self.handler.stacktrace().reverse().serialize(),
            },
            "tabs": [self.handler.scrub_data(tab.serialize()) for tab in enabled_tabs],
            "actions": [action.serialize() for action in self.actions.values()],
        }

    def render(self) -> str:
        """Render the HTML error page."""
        self.data = self.build()
        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "templates", "exceptionite.js"
        )
        with open(path, "r", encoding="utf-8") as f:
            script = f.read()

        env = Environment(loader=PackageLoader("exceptionite", "templates"))

        template = env.get_template("exception.html")
        return template.render({"data": self.data, "script": script})

    def add_tabs(self, *tab_classes: Type["Tab"]) -> "Handler":
        """Register a tab in the HTML error page."""
        for tab_class in tab_classes:
            tab = tab_class(self.handler)
            if tab.id in self.reserved_tabs and tab.id in self.tabs:
                raise ConfigurationException(
                    f"exceptionite: {tab.id} is a reserved name. This tab can't be overriden."
                )
            self.tabs.update({tab.id: tab})
        return self

    def add_actions(self, *action_classes: Type["Action"]) -> "Handler":
        """Register an action in the HTML error page."""
        for action_class in action_classes:
            action = action_class(self.handler)
            self.actions.update({action.id: action})
        return self

    def tab(self, id: str) -> "Tab":
        """Get registered tab with the given id."""
        try:
            return self.tabs[id]
        except KeyError:
            raise TabNotFound(f"Tab not found: {id}")

    def enabled_tabs(self) -> List["Tab"]:
        """Get enabled tabs from options"""
        return [
            tab
            for tab in self.tabs.values()
            if self.handler.options.get("handlers").get(tab.id, True)
        ]

    def run_action(self, action_id: str, options: dict = {}) -> dict:
        """Run the given action with options if any"""
        action = self.actions.get(action_id)
        return action.run(options)

    def add_context(self, name: str, data: "dict|Callable", icon: str = None) -> "WebRenderer":
        """Quick shortcut method to add a context block into 'context' tab."""

        custom_block = Block
        custom_block.id = f"context.id.{name.lower()}"
        custom_block.name = name
        custom_block.icon = icon
        if callable(data):
            custom_block.build = data
        else:
            custom_block.build = lambda self: data
        self.tab("context").add_blocks(custom_block)
        return self
