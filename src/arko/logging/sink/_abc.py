from abc import ABC, abstractmethod

from rich.console import Console, ConsoleRenderable

__all__ = ("AbstractSink",)


class AbstractSink(ABC):
    @abstractmethod
    def write(self, renderables: list[ConsoleRenderable]) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def tasks_to_complete(self) -> None: ...
