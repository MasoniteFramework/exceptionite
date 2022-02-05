import os
import sys
import traceback
from dotty_dict import dotty
from collections import OrderedDict

from .StackTrace import StackTrace
from .tabs import ContextTab, SolutionsTab, RecommendationsTab
from .renderers import JavascriptRenderer, TerminalRenderer


class Handler:

    reserved_tabs = ["context"]

    def __init__(
        self,
    ):
        self.renderers = {}
        self.tabs = OrderedDict()
        self.actions = {}
        self.options = dotty(
            {
                "editor": "vscode",
                "search_url": "https://www.google.com/search?q=",
                "links": {
                    "doc": "https://docs.masoniteproject.com",
                    "repo": "https://github.com/MasoniteFramework/masonite",
                },
                "stack": {"offset": 10, "shorten": True},
                "tabs": {"context": True, "solutions": True, "recommendations": True},
                "blocks": {
                    "packages_update": {"list": ["exceptionite"]},
                },
            }
        )
        self.serialized_data = None

        self.add_tab(ContextTab)
        self.add_tab(SolutionsTab)
        self.add_tab(RecommendationsTab)
        self.add_renderer("javascript", JavascriptRenderer)
        self.add_renderer("terminal", TerminalRenderer)

    def set_options(self, options):
        # ensure options is a dict here, might already be a dotty dict
        self.options = dotty(dict(options))
        return self

    def add_renderer(self, name, renderer_class):
        self.renderers.update({name: renderer_class})
        return self

    def get_renderer(self, name):
        return self.renderers[name](self)

    def add_tab(self, tab_class):
        tab = tab_class(self)
        if tab.id in self.reserved_tabs and tab.id in self.tabs:
            raise Exception(
                f"exceptionite: {tab.id} is a reserved name. This tab can't be overriden."
            )
        self.tabs.update({tab.id: tab})
        return self

    def add_action(self, action_class):
        action = action_class(self)
        self.actions.update({action.id: action})
        return self

    def get_tab(self, id):
        try:
            return self.tabs[id]
        except KeyError:
            raise Exception(f"exceptionite: Tab not found: {id}")

    def get_enabled_tabs(self):
        return [tab for tab in self.tabs.values() if self.options.get("tabs").get(tab.id, False)]

    def start(self, exception):
        """Start handling exception."""
        self._exception = exception
        self._type, self._value, self._original_traceback = sys.exc_info()
        traceback_exc = traceback.TracebackException(
            self._type, self._value, self._original_traceback, capture_locals=True
        )
        self._stacktrace = StackTrace(
            traceback_exc,
            self._exception,
            offset=self.options.get("stack.offset"),
            shorten=self.options.get("stack.shorten"),
        )
        self._stacktrace.generate().reverse()

        # save serialized exception data for further use in renderers
        self.serialized_data = self.serialize()
        return self

    # helpers
    def exception(self):
        return self._exception.__class__.__name__

    def namespace(self):
        return self._exception.__class__.__module__ + "." + self.exception()

    def message(self):
        return str(self._exception)

    def stacktrace(self):
        return self._stacktrace

    def serialize(self):
        return {
            "config": {
                **self.options.to_dict(),
                "absolute_path": os.getcwd(),
            },
            "exception": {
                "type": self.exception(),
                "message": self.message(),
                "namespace": self.namespace(),
                "stacktrace": self.stacktrace().reverse().serialize(),
            },
            "tabs": [tab.serialize() for tab in self.get_enabled_tabs()],
            "actions": [action.serialize() for action in self.actions.values()],
        }

    def render(self, renderer):
        return self.get_renderer(renderer).render()

    def get_last_exception_data(self):
        return self.serialized_data

    def run_action(self, action_id, options={}):
        action = self.actions.get(action_id)
        return action.run(options)
