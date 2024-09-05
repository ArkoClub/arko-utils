import logging
import os
import traceback
import warnings
from io import StringIO
from types import FrameType
from typing import Mapping

from arko.logging._handler import default_handler
from arko.logging._level import Level
from arko.logging._record import LogRecord
from arko.typedefs import ArgsType, ExcInfoType, SysExcInfoType

__all__ = ("Logger", "logger")


def _is_internal_frame(frame: FrameType):
    """Signal whether the frame is a CPython or logging module internal."""
    filename = os.path.normcase(frame.f_code.co_filename)
    return filename in [
        __file__,
        os.path.normcase(logging.addLevelName.__code__.co_filename),
    ] or ("importlib" in filename and "_bootstrap" in filename)


class Logger(logging.Logger):
    level: Level

    def __init__(self, name: str, level: Level | int | str = Level.NOTSET) -> None:
        level = Level[level]
        super().__init__(name, level.num)
        self.level = level

    def makeRecord(
        self,
        name: str,
        level: int | Level,
        fn: str,
        lno: int,
        msg: object,
        args: ArgsType,
        exc_info: SysExcInfoType | None,
        func: str | None = None,
        extra: Mapping[str, object] | None = None,
        sinfo: str | None = None,
    ) -> LogRecord:
        return super().makeRecord(
            name, level, fn, lno, msg, args, exc_info, func, extra, sinfo
        )

    def findCaller(
        self, stack_info: bool = False, stacklevel: int = 1
    ) -> tuple[str, int, str, str | None]:
        f = logging.currentframe()
        if not f:
            return "(unknown file)", 0, "(unknown function)", None
        while stacklevel > 0:
            next_f = f.f_back
            if next_f is None:
                break
            f = next_f
            if f.f_code.co_filename == __file__:
                stacklevel += 1
            if not _is_internal_frame(f):
                stacklevel -= 1
        co = f.f_code
        sinfo = None
        if stack_info:
            with StringIO() as sio:
                sio.write("Stack (most recent call last):\n")
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == "\n":
                    sinfo = sinfo[:-1]
        return co.co_filename, f.f_lineno, co.co_name, sinfo

    def _log(
        self,
        level: int | Level,
        msg: object,
        args: ArgsType,
        exc_info: ExcInfoType | None = None,
        extra: Mapping[str, object] | None = None,
        stack_info: bool = False,
        stacklevel: int = 1,
    ) -> None:
        return super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

    def isEnabledFor(self, level: int | Level) -> bool:
        """
        Is this logger enabled for level 'level'?
        """
        return super().isEnabledFor(level if isinstance(level, int) else level.num)

    def debug(
        self,
        msg: object,
        *args: object,
        exc_info: ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        return self._log(
            Level.DEBUG,
            msg,
            args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            stacklevel=stacklevel,
        )

    def info(
        self,
        msg: object,
        *args: object,
        exc_info: ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        return self._log(
            Level.INFO,
            msg,
            args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            stacklevel=stacklevel,
        )

    def warning(
        self,
        msg: object,
        *args: object,
        exc_info: ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        return self._log(
            Level.WARNING,
            msg,
            args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            stacklevel=stacklevel,
        )

    def warn(
        self,
        msg: object,
        *args: object,
        exc_info: ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        warnings.warn(
            "The 'warn' method is deprecated, use 'warning' instead",
            DeprecationWarning,
            2,
        )
        return self._log(
            Level.WARN,
            msg,
            args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            stacklevel=stacklevel,
        )

    def error(
        self,
        msg: object,
        *args: object,
        exc_info: ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        if self.isEnabledFor(Level.ERROR):
            return self._log(
                Level.ERROR,
                msg,
                args,
                exc_info=exc_info,
                extra=extra,
                stack_info=stack_info,
                stacklevel=stacklevel,
            )

    def exception(
        self,
        msg: object = None,
        *args: object,
        exc_info: ExcInfoType = True,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        return self._log(
            Level.ERROR,
            msg,
            args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            stacklevel=stacklevel,
        )

    def critical(
        self,
        msg: object,
        *args: object,
        exc_info: ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        return self._log(
            Level.CRITICAL,
            msg,
            args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            stacklevel=stacklevel,
        )

    def log(
        self,
        level: int | Level,
        msg: object,
        *args: object,
        exc_info: ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        return self._log(
            level,
            msg,
            args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            stacklevel=stacklevel,
        )

    def success(
        self,
        msg: object,
        *args: object,
        exc_info: ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        return self._log(
            Level.SUCCESS,
            msg,
            args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            stacklevel=stacklevel,
        )


logger = Logger("arko-logger")
logger.addHandler(default_handler)
