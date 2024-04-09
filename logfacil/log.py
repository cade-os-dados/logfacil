import logging
from types import MethodType
from functools import wraps

def activate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("Function: %s - Module: %s - Args: %s - Kwargs: %s", func.__name__, func.__module__, args, kwargs)
        return func(*args, **kwargs)
    return wrapper

def deactivate(func):
    if hasattr(func, '__wrapped__'):
        return func.__wrapped__

class Controller:

    def __init__(self):
        self.cache = dict()

    def __is_public_method__(self, tuple):
        name, attr = tuple
        is_public = type(attr) is MethodType
        is_method = not name.startswith('__')
        return is_public and is_method

    def __list_methods__(self, obj: object):
        names = dir(obj)
        attrs = map(lambda x: getattr(obj, x), names)
        methods = dict(filter(self.__is_public_method__, zip(names, attrs)))
        self.cache.update({obj: methods})
    
    def __cache_methods__(self, obj):
        if obj not in self.cache:
            self.__list_methods__(obj)
        return self.cache[obj]
    
    def ignore(self, obj, name):
        methods = self.cache.get(obj)
        if methods is not None and methods.get(name) is not None:
            setattr(obj, name, methods[name])
            methods.pop(name)
                
    def enable_logs(self, obj):
        for method, function_pointer in self.__cache_methods__(obj).items():
            setattr(obj, method, activate(function_pointer))
    
    def disable_logs(self, obj):
        for method, function_pointer in self.__cache_methods__(obj).items():
            if hasattr(getattr(obj, method), '__wrapped__'):
                setattr(obj, method, function_pointer)