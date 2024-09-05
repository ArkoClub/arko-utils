import logging
from enum import Enum, EnumType
from typing import Self, Union

from rich.style import Style

from arko.logging._style import (
    DARK_GREY,
    GREY,
    LIGHT_GREY,
    RED,
    WHITE,
    GREEN,
    YELLOW,
    BLUE,
)
from arko.wrapper import ArkoWrapper

__all__ = ("Level",)


class LevelMeta(EnumType):
    _value2member_map_: [tuple[[int, str], Enum]]

    def __getitem__(cls, item: Union[int, str, "Level"]) -> "Level":
        match item:
            case str():
                if (
                    item
                    in ArkoWrapper(
                        (i, i.lower(), i.upper()) for i in cls._member_map_.keys()
                    )
                    .flat(1)
                    .unique()
                ):
                    # noinspection PyTypeChecker
                    return (
                        cls._member_map_.get(item)
                        or cls._member_map_.get(item.lower())
                        or cls._member_map_.get(item.upper())
                    )
                raise KeyError(item)
            case int():
                return {k[0]: v for k, v in cls._value2member_map_.items()}[item]
            case Level():
                return item
            case _:
                raise KeyError(item)

    STYLE_DICT: dict[str, Style]

    def __getattr__(self, item):
        if item == "STYLE_DICT":
            return {
                f"logging.level.{k.lower()}": v.style
                for k, v in sorted(self.__members__.items(), key=lambda x: x[1].num)
            }
        else:
            # noinspection PyUnresolvedReferences
            return super().__getattr__(item)


class Level(Enum, metaclass=LevelMeta):
    num: int
    icon: str
    style: Style

    NOTSET = (0, "", Style(color=DARK_GREY, dim=True))
    TRACE = (5, ":pencil2:", Style(color=GREY))  # ✏️
    DEBUG = (10, ":bug:", Style(color=LIGHT_GREY, bold=True))  # 🐛
    INFO = (20, ":information:", Style(color=WHITE))  # ℹ️
    SUCCESS = (30, ":white_heavy_check_mark:", Style(color=GREEN))  # ✅
    WARNING = (30, ":warning:", Style(color=YELLOW))  # ⚠️
    WARN = WARNING
    ERROR = (40, ":cross_mark:", Style(color=RED))  # ❌
    CRITICAL = (50, ":pill:", Style(color=RED, bold=True, blink2=True))  # ☠️
    FATAL = CRITICAL

    def __init__(
        self, num: int = logging.NOTSET, icon: str = "", style: Style = Style.null()
    ) -> None:
        self.num = num
        self.icon = icon
        self.style = style

    def __eq__(self, other: int | Self) -> bool:
        if isinstance(other, Level) or issubclass(other.__class__, Level):
            return (
                self.num == other.num
                and self.icon == other.icon
                and self.style == other.style
            )
        elif isinstance(other, int):
            return self.num == other
        elif isinstance(other, str):
            return other in [self.name, self.name.lower()]
        else:
            raise TypeError(
                "'==' not supported between instances of "
                + f"'{self.__class__.__name__}' and '{type(other).__name__}'"
            )

    def __lt__(self, other: int | Self) -> bool:
        if isinstance(other, Level) or issubclass(other.__class__, Level):
            return self.num < other.num
        elif isinstance(other, int):
            return self.num < other
        else:
            raise TypeError(
                "'<' not supported between instances of "
                + f"'{self.__class__.__name__}' and '{type(other).__name__}'"
            )

    def __gt__(self, other: int | Self) -> bool:
        if isinstance(other, Level) or issubclass(other.__class__, Level):
            return self.num > other.num
        elif isinstance(other, int):
            return self.num > other
        else:
            raise TypeError(
                "'>' not supported between instances of "
                + f"'{self.__class__.__name__}' and '{type(other).__name__}'"
            )

    def __le__(self, other: int | Self) -> bool:
        if isinstance(other, Level) or issubclass(other.__class__, Level):
            return self.num <= other.num
        elif isinstance(other, int):
            return self.num <= other
        else:
            raise TypeError(
                "'<=' not supported between instances of "
                + f"'{self.__class__.__name__}' and '{type(other).__name__}'"
            )

    def __ge__(self, other: int | Self) -> bool:
        if isinstance(other, Level) or issubclass(other.__class__, Level):
            return self.num >= other.num
        elif isinstance(other, int):
            return self.num >= other
        else:
            raise TypeError(
                "'>=' not supported between instances of "
                + f"'{self.__class__.__name__}' and '{type(other).__name__}'"
            )

    def __int__(self) -> int:
        return self.num
