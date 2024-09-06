import logging
from datetime import datetime
from typing import TYPE_CHECKING

from rich import get_console

# noinspection PyProtectedMember
from rich._null_file import NullFile
from rich.highlighter import Highlighter, ReprHighlighter
from rich.logging import RichHandler
from rich.text import Text
from rich.theme import Theme
from typing_extensions import Iterable

from arko.funcs import resolve_path
from arko.logging._console import Console
from arko.logging._level import Level
from arko.logging._record import LogRecord
from arko.logging._render import LogRender, LogRenderConfig
from arko.logging._style import ARKO_STYLE
from arko.logging._traceback import Traceback, TracebacksConfig

if TYPE_CHECKING:
    from rich.console import ConsoleRenderable

__all__ = ("Handler", "default_handler")


class Handler(RichHandler):
    level: Level

    def __init__(
        self,
        level: Level | str | int = Level.NOTSET,
        console: Console | None = None,
        *,
        keywords: Iterable[str] | None = None,
        highlighter: Highlighter | None = None,
        enable_link_path: bool = True,
        markup: bool = False,
        rich_tracebacks: bool = False,
        traceback_config: TracebacksConfig | None = None,
        render_config: LogRenderConfig | None = None,
    ) -> None:
        level = Level[level]
        logging.Handler.__init__(self, level.num)
        self.level = level
        self.console = console or get_console()

        self.keywords = keywords or []
        self.highlighter = highlighter or ReprHighlighter()
        self.enable_link_path = enable_link_path
        self.markup = markup
        self.rich_tracebacks = rich_tracebacks

        self.traceback_config = traceback_config or TracebacksConfig()

        self._render = LogRender(render_config)

    def setLevel(self, level: int | str | Level) -> None:
        self.level = Level[level]

    def emit(self, record: LogRecord) -> None:
        message = self.format(record)
        traceback = None
        if (
            self.rich_tracebacks
            and record.exc_info
            and record.exc_info != (None, None, None)
        ):
            exc_type, exc_value, exc_traceback = record.exc_info
            assert exc_type is not None
            assert exc_value is not None
            traceback = Traceback.from_config(
                exc_type, exc_value, exc_traceback, self.traceback_config
            )
            if record.msg is not None:
                message = record.getMessage()
                if self.formatter:
                    record.message = record.getMessage()
                    formatter = self.formatter
                    if hasattr(formatter, "usesTime") and formatter.usesTime():
                        record.asctime = formatter.formatTime(record, formatter.datefmt)
                    message = formatter.formatMessage(record)
            else:
                message = ""

        message_renderable = self.render_message(record, message)
        log_renderables = self.render(
            record=record, traceback=traceback, message_renderable=message_renderable
        )
        if isinstance(self.console.file, NullFile):
            self.handleError(record)
        else:
            # noinspection PyBroadException
            try:
                for log_renderable in log_renderables:
                    self.console.print(log_renderable)
            except Exception:  # NOSONAR
                self.handleError(record)

    def render_message(self, record: LogRecord, message: str) -> "ConsoleRenderable":
        use_markup: bool = getattr(record, "markup", self.markup)
        style = record.level.style if hasattr(record, "level") else ""
        message_text = (
            Text.from_markup(message) if use_markup else Text(message, style=style)
        )

        highlighter: "Highlighter" = getattr(record, "highlighter", self.highlighter)
        if highlighter:
            message_text = highlighter(message_text)

        self.keywords = self.keywords or []

        if self.keywords:
            message_text.highlight_words(self.keywords, "logging.keyword")

        return message_text

    def render(
        self,
        *,
        record: LogRecord,
        traceback: Traceback | None,
        message_renderable: "ConsoleRenderable",
    ) -> list["ConsoleRenderable"]:
        path = resolve_path(record.pathname)
        level = self.get_level_text(record)
        time_format = None if self.formatter is None else self.formatter.datefmt
        log_time = datetime.fromtimestamp(record.created)

        renderables = []
        if message_renderable:
            renderables.append(message_renderable)
        if traceback:
            renderables.append(traceback)

        log_renderable = self._render(
            self.console,
            renderables,
            log_time=log_time,
            time_format=time_format,
            level=record.level,
            level_text=level,
            path=path,
            line_no=record.lineno,
            link_path=record.pathname if self.enable_link_path else None,
        )
        # noinspection PyTypeChecker
        return log_renderable


default_handler = Handler(
    Level.NOTSET, Console(theme=Theme(ARKO_STYLE)), rich_tracebacks=True
)
