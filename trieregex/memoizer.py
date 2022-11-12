from functools import wraps
from typing import Any, Callable, Dict, MutableMapping, Protocol, TypeVar

R = TypeVar('R')

class CacheProtocol(Protocol[R]):
    cache: MutableMapping[str, R]

    def __call__(self, *args: Any, **kwds: Any) -> R:
        ...

    def clear_cache(self) -> None:
        ...


def memoizer() -> Callable[[Callable[..., R]], CacheProtocol[R]]:
    """Decorator function for increasing the processing speed of a function using 
    memoization with cache-clearing capability
    """

    def decorator(func: Callable[..., R]) -> CacheProtocol[R]:
        cache: Dict[str, Any] = {}

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            stringed = str(args)
            if stringed not in cache:
                cache[stringed] = func(*args, **kwargs)
            return cache[stringed]

        wrapper.__name__ = f'[Memoizer-decorated function] {func.__name__}'
        wrapper.__doc__ = f'[Memoizer-decorated function] {func.__doc__}'
        wrapper.cache = cache  # type: ignore
        wrapper.clear_cache = lambda: cache.clear()  # type: ignore
        return wrapper  # type: ignore

    return decorator
