import logging

level = logging.INFO
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

def retry(times: int):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times
    :param times: The number of times to repeat the wrapped function/method
    :type times: int times to retry running this
    """

    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(
                        f"Exception '{e}' thrown when running '{func}' (attempt {attempt} of {times} times)"
                    )
                    attempt += 1
            return func(*args, **kwargs)

        return newfn

    return decorator