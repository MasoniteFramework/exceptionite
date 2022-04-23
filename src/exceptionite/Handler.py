import sys
import traceback
from dotty_dict import dotty
from typing import Type, TYPE_CHECKING
from typing_extensions import Protocol

if TYPE_CHECKING:

    class Renderer(Protocol):
        handler: "Handler"

        def __init__(self, handler: "Handler") -> None:
            ...

        def render(self) -> str:
            """Render exception with the given renderer"""
            ...


from .StackTrace import StackTrace
from .renderers import WebRenderer, TerminalRenderer, JSONRenderer
from .options import DEFAULT_OPTIONS as DefaultOptions


class Handler:
    """Exceptionite handler used to handle exceptions and render them using the given renderer."""

    scrub_keywords = [
        "password",
        "passwd",
        "pwd",
        "secret",
        "key",
        "api_key",
        "apikey",
        "access_token",
        "credentials",
        "token",
    ]

    def __init__(
        self,
    ):
        self.renderers: dict["Renderer"] = {}
        self.options: dict = dotty(DefaultOptions)
        self.context = {}
        self.add_renderer("web", WebRenderer)
        self.add_renderer("terminal", TerminalRenderer)
        self.add_renderer("json", JSONRenderer)

    def set_options(self, options: dict) -> "Handler":
        """Configure exceptionite handler with given options."""
        # ensure options is a dict here, might already be a dotty dict
        self.options = dotty(dict(options))
        return self

    def add_renderer(self, name: str, renderer_class: Type["Renderer"]) -> "Handler":
        """Register a renderer to handle exceptions."""
        self.renderers.update({name: renderer_class(self)})
        return self

    def renderer(self, name: str) -> "Renderer":
        """Get the renderer with the given name."""
        return self.renderers[name]

    def add_context(self, name: str, data: dict) -> "Handler":
        self.context.update({name: data})
        return self

    def start(self, exception: BaseException) -> "Handler":
        """Start handling the given exception."""
        self._exception = exception
        self._type, self._value, self._original_traceback = sys.exc_info()
        traceback_exc = traceback.TracebackException(
            self._type, self._value, self._original_traceback, capture_locals=True
        )
        self._stacktrace = StackTrace(
            traceback_exc,
            self._exception,
            offset=self.options.get("options.stack.offset"),
            shorten=self.options.get("options.stack.shorten"),
            scrubber=self.scrub_data,
        )
        self._stacktrace.generate().reverse()
        return self

    # helpers
    def exception(self) -> str:
        """Get the handled exception name."""
        return self._exception.__class__.__name__

    def namespace(self) -> str:
        """Get the handled exception full namespace."""
        return self._exception.__class__.__module__ + "." + self.exception()

    def message(self) -> str:
        """Get the handled exception message."""
        return str(self._exception)

    def stacktrace(self) -> "StackTrace":
        """Get the handled exception stack trace object."""
        return self._stacktrace

    def count(self):
        return len(self._stacktrace)

    def render(self, renderer: str) -> str:
        """Render the handled exception with the given renderer."""
        return self.renderer(renderer).render()

    def add_scrub_keywords(self, keywords: list) -> "Handler":
        """Add new scrub keywords used to hide sensitive data."""
        self.scrub_keywords.extend(keywords)
        # ensure keywords are not duplicated
        self.scrub_keywords = list(set(self.scrub_keywords))
        return self

    def set_scrub_keywords(self, keywords: list) -> "Handler":
        """Override scrub keywords used to hide sensitive data."""
        self.scrub_keywords = keywords
        return self

    def scrub_data(self, data: dict, disable: bool = False) -> dict:
        """Hide sensitive data of the given dictionary if enabled in the options with
        'hide_sensitive_data' parameter."""
        if not self.options.get("options.hide_sensitive_data") or disable:
            return data
        scrubbed_data = {}
        if not data:
            return scrubbed_data
        for key, val in data.items():
            if not val:
                scrubbed_data[key] = val
                continue
            if isinstance(val, dict):
                scrubbed_data[key] = self.scrub_data(val, disable)
            else:
                # scrub entire value if key matches
                should_scrub = False
                for token in self.scrub_keywords:
                    if token.lower() in key.lower():
                        should_scrub = True
                if should_scrub:
                    scrubbed_val = "*****"
                else:
                    scrubbed_val = val
                scrubbed_data[key] = scrubbed_val
        return scrubbed_data
