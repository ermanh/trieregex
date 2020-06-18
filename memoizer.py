def memoizer(func):
    cache = {}
    def function_wrapper(*arg):
        stringed = str(arg[1:])  # exclude self
        if stringed in cache:
            return cache[stringed]
        cache[stringed] = func(*arg)
        return cache[stringed]

    return function_wrapper
