from rich.color import ColorSystem
from rich.console import (
    Console as RichConsole,
    detect_legacy_windows,
)

from arko.const import IS_RUNNING_IN_PYCHARM

__all__ = ("Console",)


class Console(RichConsole):
    def __init__(self, *args, legacy_windows: bool | None = None, **kwargs) -> None:
        super().__init__(*args, legacy_windows=legacy_windows, **kwargs)
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
