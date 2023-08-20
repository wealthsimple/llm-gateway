import logging

level = logging.INFO
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)


def max_retries(times: int, exceptions: tuple = (Exception)):
    """
    Max Retry Decorator
    Retries the wrapped function/method `times` times
    :param times: The max number of times to repeat the wrapped function/method
    :type times: int
    :param Exceptions: Lists of exceptions that trigger a retry attempt
    :type Exceptions: List of Exceptions
    """

    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.error(
                        f"Exception '{e}' thrown when running '{func}'"
                        + f"(attempt {attempt} of {times} times)"
                    )
                    attempt += 1
            return func(*args, **kwargs)

        return newfn

    return decorator
