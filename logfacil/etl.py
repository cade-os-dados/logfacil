import logging
from functools import wraps

import inspect

def log_arguments(func, *args, **kwargs):
    sig = inspect.signature(func)
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()

    string = ""

    for name, value in bound_args.arguments.items():
        if hasattr(value, "shape"):
            string+=f"{name} = {value.shape}"

    return string


class LogMessage:
    def __init__(self, header, func):
        self.header = header
        self.func_name = func.__name__
        self.module_name = func.__module__
        self.file_name = func.__code__.co_filename
        self.line_number = func.__code__.co_firstlineno


    def write(self, msg) -> str:
        return (
            f"{self.header:<10} | "
            f"Func: {self.func_name:<10} | "
            f"{msg:<50} | "
            f"Module: {self.module_name:<10} | "
            f"File: {self.file_name}:{self.line_number}"
        )

def log_begin(log: LogMessage):
    logging.info(log.write("Begin"))

def log_return(valor, log: LogMessage):
    if valor is None:
        logging.critical(log.write("End - Return value is None"))
    else:
        if(hasattr(valor,'shape')):
            logging.info(log.write(f"End - Return value has shape: {valor.shape}"))
        else:
            logging.warning(log.write("End - Return value has no attribute shape"))

def log_etl_extract(func):
    'This wrapper expects that return value is a Pandas DataFrame'
    @wraps(func)
    def wrapper(*args, **kwargs):
        log = LogMessage("[EXTRACT]", func)
        log_begin(log)
        valor = func(*args, **kwargs)
        log_return(valor,log)
        return valor
    return wrapper

def log_etl_transform(func):
    'This wrapper expects that return value is a Pandas DataFrame'
    @wraps(func)
    def wrapper(*args, **kwargs):
        log = LogMessage("[TRANSFORM]", func)
        log_begin(log)
        
        log_args = log_arguments(func,*args,**kwargs)
        if len(log_args):
            msg = 'Identified DataFrames with shapes: '+log_args
            logging.info(log.write(msg))

        valor = func(*args, **kwargs)
        log_return(valor,log)
        return valor
    return wrapper

def deactivate(func):
    if hasattr(func, '__wrapped__'):
        return func.__wrapped__
