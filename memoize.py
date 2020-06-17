cache = {}

def memoize(func):
    global cache
    def function_wrapper(arg1, arg2):
        stringed = str(arg1) + str(arg2)
        if stringed in cache:
            return cache[stringed]
        cache[stringed] = func(arg1, arg2)
        return cache[stringed]
    return function_wrapper
