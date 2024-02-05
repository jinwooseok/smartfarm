from functools import wraps
from .validators import serializer_validator


def valid_serializer(view_func):
    @wraps(view_func)
    def _wrapped_view(serializer, *args, **kwargs):
        serializer = serializer_validator(serializer)
        return view_func(serializer, *args, **kwargs)
    
    return _wrapped_view

def logging_time(original_fn):
    import time
    from functools import wraps

    @wraps(original_fn)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)

        end_time = time.time()
        print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time - start_time))
        return result
    return wrapper