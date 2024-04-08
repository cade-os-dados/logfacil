import logging
from functools import wraps

def activate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("Function: %s - Module: %s", func.__name__, func.__module__)
        return func(*args, **kwargs)
    return wrapper