from multiprocessing import RLock as Lock
from typing import (
    ClassVar,
    TYPE_CHECKING,
)

from typing_extensions import Self

if TYPE_CHECKING:
    from multiprocessing.synchronize import RLock as LockType

__all__ = ("singleton", "Singleton")


class _Singleton[T]:
    lock: ClassVar["LockType"] = Lock()

    __slots__ = "cls", "instance"

    cls: type[T]
    instance: T | None

    def __init__(self, cls: type[T]):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs) -> T:
        with self.lock:
            if self.instance is None or args or kwargs:
                self.instance = self.cls(*args, **kwargs)
        return self.instance


def singleton[T](cls: type[T] | None = None) -> type[T]:
    def wrap(_cls: type[T]) -> _Singleton[T]:
        return _Singleton(_cls)

    return wrap if cls is None else wrap(cls)


class Singleton(object):
    _lock: ClassVar["LockType"] = Lock()
    _instance: ClassVar[Self | None] = None

    def __new__(cls, *args, **kwargs) -> Self:
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
