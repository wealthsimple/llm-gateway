# llm-gateway - A proxy service in front of llm models to encourage the
# responsible use of AI.
#
# Copyright 2023 Wealthsimple Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import traceback
from functools import wraps
from typing import Any, Callable, Dict, Iterator, List, TypeVar

from fastapi import HTTPException

from llm_gateway.logger import get_logger

T = TypeVar("T")

logger = get_logger(__name__)


def max_retries(times: int, exceptions: tuple = (Exception,)):
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


class StreamProcessor:
    def __init__(
        self, stream_processor: Callable[[Iterator[T]], Iterator[Dict[str, Any]]]
    ) -> None:
        self.stream_processor = stream_processor
        self.cached_streamed_response: List[Dict[str, Any]] = []

    def process_stream(self, response: Iterator[T]) -> Iterator[Dict[str, Any]]:
        for item in self.stream_processor(response):
            self.cached_streamed_response.append(item)
            yield item

    def get_cached_streamed_response(self) -> List[Dict[str, Any]]:
        return self.cached_streamed_response


def reraise_500(func: Callable) -> Callable:
    """
    Decorator to ensure routes return informative error messages
    when encountering an internal error. Provides a sensible default,
    but will be overwritten if the route provides a specific HTTP exception.

    Always put this decorator as the bottom decorator. Otherwise, the fastapi
    router decorator will overpower it.

    :param func: Callable to be decorated
    :type func: Callable
    :raises HTTPException: If there is any error raise HTTP 500 and log to DataDog
    :return: Decorated callable
    :rtype: Callable
    """

    # stops function signature from being overwritten
    @wraps(func)
    def wrapper(*args: Any, **kwargs: dict) -> None:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # If the route is already raising a specific HTTPException,
            # use it instead of overriding with our 500 code
            if isinstance(e, HTTPException):
                raise e
            else:
                logger.error(traceback.format_exc())
                raise HTTPException(
                    status_code=500,
                    detail=f"Internal error due to: {str(e)}",
                )

    return wrapper
