import functools


def check_arguments(*expected_types):
    def wrapper_1(func):
        @functools.wraps(func)
        def wrapper_2(*args):
            if (len(args) < len(expected_types)):
                raise TypeError
            for i, type in enumerate(expected_types):
                if not isinstance(args[i], type):
                    raise TypeError
            return func(*args)
        return wrapper_2
    return wrapper_1
