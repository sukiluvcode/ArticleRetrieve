import logging
import functools


def log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Set up logging
        logger = logging.getLogger(func.__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # Log function call
        logger.info(f"Function {func.__name__} called with args: {args}, kwargs: {kwargs}")
        # Call the function and log the return value
        result = func(*args, **kwargs)
        logger.info(f"Function {func.__name__} returned: {result}")

        return result

    return wrapper

@log_decorator
def add(a, b):
    return a + b

add(4, 6)