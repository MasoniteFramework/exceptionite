from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Handler import Handler


class JSONRenderer:
    """Renderer used to render exception as JSON payload."""

    def __init__(self, handler: "Handler") -> None:
        self.handler = handler
        self.data: dict = {}

    def build(self):
        return {
            "exception": {
                "type": self.handler.exception(),
                "namespace": self.handler.namespace(),
            },
            "message": self.handler.message(),
            "stacktrace": self.handler.stacktrace().reverse().serialize_light(),
        }

    def render(self) -> str:
        """Render the JSON payload."""
        self.data = self.build()
        return self.data
