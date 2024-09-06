import asyncio
import sys
import traceback
from asyncio import AbstractEventLoop, Task
from contextvars import Context
from typing import Awaitable, Callable
from weakref import WeakSet

from rich.console import ConsoleRenderable

from arko.logging._console import Console
from arko.logging.sink._abc import AbstractSink

__all__ = ("StandardSink", "AsyncSink", "CallableSink")


class StandardSink(AbstractSink):
    _console: Console

    @property
    def console(self) -> Console:
        return self._console

    def __init__(self, *args, **kwargs) -> None:
        self._console = Console(*args, **kwargs)

    def write(self, renderables: list[ConsoleRenderable]) -> None:
        self.console.print(*renderables)

    def stop(self) -> None:
        self.console.quiet = True

    def tasks_to_complete(self) -> None:
        """Do Nothing"""


class AsyncSink(AbstractSink):
    @property
    def loop(self) -> AbstractEventLoop:
        return self._loop or asyncio.get_running_loop()

    def __init__(
        self,
        function: Callable[[list[ConsoleRenderable]], Awaitable[None]],
        *,
        catch_error: bool = True,
        loop: AbstractEventLoop | None = None,
    ) -> None:
        self._function = function
        self._catch_error = catch_error
        self._loop = loop
        self._tasks: WeakSet[Task] = WeakSet()

    def write(self, renderables: list[ConsoleRenderable]) -> None:
        coroutine = self._function(renderables)
        task = self.loop.create_task(coroutine)

        def check_exception(future: Task, *, _: Context | None = None):
            exception = future.exception()
            if future.cancelled() or exception is None:
                return
            if not self._catch_error:
                raise future.exception()

            if not sys.stderr:
                return

            if exception is None:
                type_, value, traceback_ = sys.exc_info()
            else:
                type_, value, traceback_ = (
                    type(exception),
                    exception,
                    exception.__traceback__,
                )

            try:
                sys.stderr.write("--- Logging Error ---\n")
                # noinspection PyBroadException
                try:
                    record_repr = "\n".join(map(str, renderables))
                except Exception:
                    record_repr = "/!\\ Unprintable record /!\\"
                sys.stderr.write("Record was: %s\n" % record_repr)
                traceback.print_exception(type_, value, traceback_, None, sys.stderr)
                sys.stderr.write("--- End of logging error ---\n")
            except OSError:
                pass
            finally:
                del type_, value, traceback_

        task.add_done_callback(check_exception)
        self._tasks.add(task)

    def stop(self) -> None:
        for task in filter(lambda t: not t.cancelled(), self._tasks):
            task.cancel()

    def tasks_to_complete(self) -> None:
        for task in self._tasks:
            if task.get_loop() != self.loop:
                continue
            self.loop.run_until_complete(task)


class CallableSink(AbstractSink):
    def __init__(self, function: Callable[[list[ConsoleRenderable]], None]) -> None:
        self._function = function

    def write(self, renderables: list[ConsoleRenderable]) -> None:
        self._function(renderables)

    def stop(self) -> None:
        """Do Nothing"""

    def tasks_to_complete(self) -> None:
        """Do Nothing"""
