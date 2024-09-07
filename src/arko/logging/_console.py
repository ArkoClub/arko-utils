from rich.color import ColorSystem
from rich.console import (
    Console as RichConsole,
    detect_legacy_windows,
)
from rich.default_styles import DEFAULT_STYLES
from rich.theme import Theme

from arko.const import IS_RUNNING_IN_PYCHARM
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
