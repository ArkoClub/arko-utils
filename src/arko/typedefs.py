from pathlib import Path
from types import TracebackType
from typing import Literal, Mapping, TypeAlias, Union

StrOrPath = Union[Path, str]

SysExcInfoType: TypeAlias = (
    tuple[type[BaseException], BaseException, TracebackType | None]
    | tuple[None, None, None]
)
ExcInfoType: TypeAlias = None | bool | SysExcInfoType | BaseException
ArgsType: TypeAlias = tuple[object, ...] | Mapping[str, object]
FormatStyle: TypeAlias = Literal["%", "{", "$"]
