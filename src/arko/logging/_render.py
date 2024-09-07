from datetime import datetime, timedelta
from typing import Callable, Iterable, TYPE_CHECKING

from markdown_it.rules_block import table
from pydantic_settings import BaseSettings
from rich.containers import Renderables
from rich.table import Table
from rich.text import Text, TextType

from arko.logging._level import Level
from arko.const import IS_RUNNING_IN_PYCHARM

if TYPE_CHECKING:
    from rich.console import ConsoleRenderable, RenderableType

__all__ = ("LogRenderConfig", "LogRender")


FormatTimeCallable = Callable[[datetime], Text]


class LogRenderConfig(BaseSettings):
    show_time: bool = True
    show_level: bool = True
    show_level_icon: bool = True
    show_path: bool = True
    newline_time: bool = True
    time_format: str | FormatTimeCallable = "[%y/%m/%d %X]"
    omit_times_part: bool = True
    omit_times_part_interval: float = 0.5
    level_width: int | None = None


class LogRender:
    def __init__(self, config: LogRenderConfig | None = None) -> None:
        self._config = config or LogRenderConfig()
        self._last_time: datetime | None = None

    def __call__(
        self,
        renderables: Iterable["ConsoleRenderable"],
        log_time: datetime | None = None,
        time_format: str | FormatTimeCallable | None = None,
        level: Level | None = None,
        level_text: TextType = "",
        path: str | None = None,
        line_no: int | None = None,
        link_path: bool | None = None,
    ) -> list[Table]:
        link_path = link_path and not IS_RUNNING_IN_PYCHARM

        level = level or Level.NOTSET

        output_time = None
        output_main = Table.grid(padding=(0, 1), pad_edge=True)
        output_main.expand = True

        result = [output_main]

        if self._config.show_time:
            if self._config.newline_time:
                output_time = Table.grid(padding=(1, 1, 0, 1), pad_edge=True)
                output_time.add_column(style="log.time")
                result.insert(0, output_time)
            else:
                output_main.add_column(style="log.time")

        if self._config.show_level_icon:
            output_main.add_column(width=2)

        if self._config.show_level:
            output_main.add_column(
                style="log.level",
                width=self._config.level_width
                or max(map(len, Level.__members__.keys())),
                justify="left",
            )

        output_main.add_column(ratio=1, style="log.message", overflow="fold")

        if self._config.show_path and path:
            output_main.add_column(justify="right")

        row: list["RenderableType"] = []
        if self._config.show_time:
            log_time = log_time or datetime.now()
            time_format = time_format or self._config.time_format

            if callable(time_format):
                log_time_display = time_format(log_time)
            else:
                log_time_display = Text(log_time.strftime(time_format))

            if (
                self._config.omit_times_part
                and self._last_time
                and (
                    (log_time - self._last_time)
                    <= timedelta(seconds=self._config.omit_times_part_interval)
                )
            ):
                log_time_display = Text(" " * len(log_time_display))
                if not self._config.newline_time:
                    row.append(log_time_display)
            else:
                self._last_time = log_time
                if self._config.newline_time:
                    output_time.add_row(log_time_display)
                else:
                    row.append(log_time_display)

        if self._config.show_level_icon:
            row.append(level.icon)

        if self._config.show_level:
            row.append(level_text)

        row.append(Renderables(renderables))
        if self._config.show_path and path:
            path_style = f"link file://{link_path}" if link_path else ""
            if line_no:  # 如果显示行号
                line_no_style = (
                    f"link file://{link_path}#{line_no}" if link_path else ""
                )

                path_table = Table.grid(pad_edge=True)
                path_table.add_column(style="log.path", justify="right")  # 路径
                path_table.add_column()  # 分隔符
                path_table.add_column(style="log.line_no", justify="left")  # 行号

                path_table.add_row(
                    Text(path, style=path_style),
                    ":",
                    Text(str(line_no), style=line_no_style),
                )

                row.append(path_table)
            else:  # 如果不显示行号
                row.append(Text(path, style=path_style))

        output_main.add_row(*row)
        return list(filter(bool, result))
