import re

def memoizer(func):
    cache = {}
    def function_wrapper(*arg):
        stringed = str(arg[1:])  # exclude self
        if stringed in cache:
            return cache[stringed]
        cache[stringed] = func(*arg)
        return cache[stringed]
    return function_wrapper

def validate_boundaries(before, after, initials, finals):
    if before == '' and after == '':
        pass
    if before != '' and after == '':
        if before == '\\b':
            if re.search('^\w', ''.join(initials)):
                raise ValueError('\\b' )
