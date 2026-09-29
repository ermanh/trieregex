from functools import partial
from typing import Any, Callable, Dict, Tuple, Type


def _cache_part(value):
    # type: (Any) -> Any
    try:
        hash(value)
        return value
    except TypeError:
        return (type(value).__name__, id(value))


class Memoizer:
    """Decorator class for increasing the processing speed of a function using 
    memoization with cache-clearing capability
    """
    __slots__ = ['func', 'cache']

    def __init__(self, func):
        # type: (Callable) -> None
        self.func = func
        self.cache = {}  # type: Dict[Tuple[Any, ...], Any]

    def __call__(self, *args):
        # type: (Any) -> Any
        # Prefer instance._uid over str(instance): heap addresses are reused, so
        # "object at 0xADDR" can collide across distinct TrieRegEx instances.
        inst = args[0] if args else None
        uid = getattr(inst, "_uid", None)
        rest = tuple(_cache_part(a) for a in args[1:])
        key = (uid,) + rest if uid is not None else tuple(_cache_part(a) for a in args)
        if key not in self.cache:
            self.cache[key] = self.func(*args)
        return self.cache[key]

    def __get__(self, instance, owner):
        # type: (object, Type) -> Callable
        fn = partial(self.__call__, instance)
        fn.__name__ = f'[Memoizer-decorated function] {self.func.__name__}'
        fn.__doc__ = f'[Memoizer-decorated function] {self.func.__doc__}'
        fn.clear_cache = self._clear_cache
        return fn

    def _clear_cache(self):
        # type: () -> None
        self.cache.clear()
