import os
import logging
from datetime import datetime

def valid_log_dir(dir: str):
    if not os.path.isdir(dir):
        os.makedirs(dir)

def log_file(path: str):
    'If log file path isnt defined, define as date today .log'
    if path == '':
        path = f"{datetime.now().strftime('%Y-%m-%d')}.log"
    return path

# Configure the logging system
def init(path: str = '', dir: str = './logs'):

    path = log_file(path)

    # create dir if not exists
    valid_log_dir(dir)

    # join dir and path
    log_path = os.path.join(dir,path)

    # salvar os handlers
    handlers = [
        logging.FileHandler(log_path) # Log to a file
        #logging.StreamHandler()  # Log to the console
    ]

    # config log
    logging.basicConfig(
        level=logging.INFO,  # Set the desired log level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

    return handlers

def close_all(handlers):
    for handler in handlers:
        handler.close()