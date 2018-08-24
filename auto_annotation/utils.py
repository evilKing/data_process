#coding: utf-8

from functools import wraps

func2t = []
def debugger(prefix=''):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global func2t
            res = func(*args, **kwargs)
            func_str = '%s.%s \t %s' % (prefix, func.__name__, func.__doc__)

            func2t.append(func_str)
            return res

        return wrapper

    return decorator

def print_res():
    for func in func2t:
        print(func)

