from rich.color import ColorSystem
from rich.console import (
    Console as RichConsole,
    JustifyMethod,
    NO_CHANGE,
    NewLine,
    OverflowMethod,
    detect_legacy_windows,
)
from rich.default_styles import DEFAULT_STYLES
from rich.segment import Segment
from rich.style import Style
from rich.theme import Theme

from arko.const import IS_RUNNING_IN_PYCHARM, IS_WINDOWS
from arko.logging._style import ARKO_STYLE

__all__ = ("Console",)


class Console(RichConsole):
    def __init__(
        self,
        *args,
        theme: Theme | None = None,
        legacy_windows: bool | None = None,
        **kwargs,
    ) -> None:
        theme = Theme(
            ARKO_STYLE | (theme.styles if theme is not None else DEFAULT_STYLES)
        )
        super().__init__(*args, theme=theme, legacy_windows=legacy_windows, **kwargs)
        self.legacy_windows: bool = (
            (
                detect_legacy_windows()
                and not self.is_jupyter
                and not IS_RUNNING_IN_PYCHARM
            )
            if legacy_windows is None
            else legacy_windows
        )

    def _detect_color_system(self) -> ColorSystem | None:
        if IS_RUNNING_IN_PYCHARM:
            return ColorSystem.EIGHT_BIT
        else:
            return super()._detect_color_system()

    def _get_rendered_buffer(
        self,
        *objects,
        sep: str = " ",
        end: str = "\n",
        style: str | Style | None = None,
        justify: JustifyMethod | None = None,
        overflow: OverflowMethod | None = None,
        no_wrap: bool | None = None,
        emoji: bool | None = None,
        markup: bool | None = None,
        highlight: bool | None = None,
        width: int | None = None,
        height: int | None = None,
        crop: bool = True,
        soft_wrap: bool | None = None,
        new_line_start: bool = False,
    ) -> list[Segment]:
        objects = (NewLine(),) if not objects else objects
        soft_wrap = self.soft_wrap if soft_wrap is None else soft_wrap

        if soft_wrap:
            no_wrap = True if no_wrap is None else no_wrap
            overflow = "ignore" if overflow is None else overflow
            crop = False

        renderables = self._collect_renderables(
            objects,
            sep,
            end,
            justify=justify,
            emoji=emoji,
            markup=markup,
            highlight=highlight,
        )
        # noinspection PyTypeChecker
        render_options = self.options.update(
            justify=justify,
            overflow=overflow,
            width=min(width, self.width) if width is not None else NO_CHANGE,
            height=height,
            no_wrap=no_wrap,
            markup=markup,
            highlight=highlight,
        )

        new_segments: list[Segment] = []
        extend = new_segments.extend
        render = self.render
        if style is None:
            for renderable in renderables:
                extend(render(renderable, render_options))
        else:
            for renderable in renderables:
                extend(
                    Segment.apply_style(
                        render(renderable, render_options), self.get_style(style)
                    )
                )
        if new_line_start and (
            len("".join(segment.text for segment in new_segments).splitlines()) > 1
        ):
            new_segments.insert(0, Segment.line())

        buffer: list[Segment] = []

        if crop:
            buffer_extend = buffer.extend
            for line in Segment.split_and_crop_lines(
                new_segments, self.width, pad=False
            ):
                buffer_extend(line)
        else:
            buffer.extend(new_segments)
        return buffer

    def render_to_str(
        self,
        *objects,
        sep: str = " ",
        end: str = "\n",
        style: str | Style | None = None,
        justify: JustifyMethod | None = None,
        overflow: OverflowMethod | None = None,
        no_wrap: bool | None = None,
        emoji: bool | None = None,
        markup: bool | None = None,
        highlight: bool | None = None,
        width: int | None = None,
        height: int | None = None,
        crop: bool = True,
        soft_wrap: bool | None = None,
        new_line_start: bool = False,
    ) -> str:
        buffer: list[Segment] = self._get_rendered_buffer(
            *objects,
            sep=sep,
            end=end,
            style=style,
            justify=justify,
            overflow=overflow,
            no_wrap=no_wrap,
            emoji=emoji,
            markup=markup,
            highlight=highlight,
            width=width,
            height=height,
            crop=crop,
            soft_wrap=soft_wrap,
            new_line_start=new_line_start,
        )

        result = ""

        if IS_WINDOWS:
            text = self._render_buffer(buffer[:])
            max_write = 32 * 1024 // 4
            if len(text) <= max_write:
                result += text
            else:
                batch: list[str] = []
                batch_append = batch.append
                size = 0
                for line in text.splitlines(True):
                    if size + len(line) > max_write and batch:
                        result += "".join(batch)
                        batch.clear()
                        size = 0
                    batch_append(line)
                    size += len(line)
                if batch:
                    result += "".join(batch)
                    batch.clear()
        else:
            result += self._render_buffer(buffer[:])

        return result[:-1] if result[-1] == "\n" and result else result
