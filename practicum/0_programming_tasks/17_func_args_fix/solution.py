import functools


def substitutive(func):
    @functools.wraps(func)
    def wrapper(*args):
        defs = func.__defaults__
        if defs is None:
            defs = ()
        if len(args) >= (func.__code__.co_argcount - len(defs)):
            return func(*args)
        else:
            @functools.wraps(func)
            def func_1(*extra_args):
                return wrapper(*(args + extra_args))
            return func_1
    return wrapper
