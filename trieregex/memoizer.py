from functools import partial


class Memoizer:
    __slots__ = ['func', 'cache']

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        stringed = str(args)
        if stringed not in self.cache:
            self.cache[stringed] = self.func(*args)
        return self.cache[stringed]

    def __get__(self, obj, objtype):
          fn = partial(self.__call__, obj)
          fn.clear_cache = self._clear_cache
          return fn

    def _clear_cache(self):
        self.cache.clear()
