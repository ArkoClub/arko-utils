import logging
from typing import Any, Mapping

from arko.logging._record import LogRecord
from arko.typedefs import FormatStyle


__all__ = ("Formatter", "default_formatter")


class Formatter(logging.Formatter):
    def __init__(
        self,
        fmt: str | None = None,
        date_fmt: str | None = None,
        style: FormatStyle = "%",
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(fmt, date_fmt, style, validate, defaults=defaults)

    def formatMessage(self, record: LogRecord) -> str:
        return self._style.format(record)


default_formatter = Formatter()
