import logging

level = logging.INFO
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)


def max_retries(times: int):
    """
    Max Retry Decorator
    Retries the wrapped function/method `times` times
    :param times: The max number of times to repeat the wrapped function/method
    :type times: int
    """

    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(
                        f"Exception '{e}' thrown when running '{func}'"
                        + f"(attempt {attempt} of {times} times)"
                    )
                    attempt += 1
            return func(*args, **kwargs)

        return newfn

    return decorator
