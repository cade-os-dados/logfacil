import logging
from types import MethodType
from functools import wraps

def _is_pandas_object(obj):
    tipo = type(obj)
    return tipo.__name__ in ('DataFrame', 'Series') and tipo.__module__.startswith('pandas')

def activate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Exemplo: filtrando ou formatando os args caso sejam do Pandas
        args_formatados = [
            f"<{type(arg).__name__} shape={arg.shape}>" if _is_pandas_object(arg) else arg
            for arg in args
        ]
        kwargs_formatados = [
            f"<{type(kwarg).__name__} shape={kwarg.shape}>" if _is_pandas_object(kwarg) else kwarg
            for kwarg in kwargs
        ]

        logging.info("Function: %s - Module: %s - Args: %s - Kwargs: %s", func.__name__, func.__module__, args_formatados, kwargs_formatados)
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
        self.cache.update({id(obj): methods})
    
    def __cache_methods__(self, obj):
        if id(obj) not in self.cache:
            self.__list_methods__(obj)
        return self.cache[id(obj)]
    
    def ignore(self, obj, name):
        methods = self.cache.get(id(obj))
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