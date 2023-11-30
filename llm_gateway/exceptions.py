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

from cohere.error import CohereAPIError, CohereConnectionError, CohereError
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from openai.error import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    RateLimitError,
    Timeout,
    TryAgain,
)

from llm_gateway.logger import get_logger

OPENAI_EXCEPTIONS = (
    Timeout,
    APIError,
    APIConnectionError,
    TryAgain,
    RateLimitError,
    AuthenticationError,
)
COHERE_EXCEPTIONS = (CohereError, CohereAPIError, CohereConnectionError)

logger = get_logger(__name__)


class OpenAIRouteExceptionHandler(APIRoute):
    """
    This is a route class override for the OpenAI router. It is used to
    catch common exceptions that are raised by the OpenAI API and return an
    internal server error response with its associated error message.
    """

    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def exception_handler(request: Request) -> JSONResponse:
            """
            Catch OpenAI exceptions and return an internal server error response.

            :param request: The request object
            :type request: Request
            :return: Internal server error response with error message
            :rtype: JSONResponse
            """
            try:
                response = await original_route_handler(request)
            except OPENAI_EXCEPTIONS as e:
                # print exception traceback to console
                logger.exception(type(e), e, e.__traceback__)
                raise HTTPException(
                    status_code=500,
                    detail=str(e),
                )
            return response

        return exception_handler


class CohereRouteExceptionHandler(APIRoute):
    """
    This is a route class override for the Cohere router. It is used to
    catch common exceptions that are raised by the Cohere API and return an
    internal server error response with its associated error message.
    """

    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def exception_handler(request: Request) -> JSONResponse:
            """
            Catch Cohere exceptions and return an internal server error response.

            :param request: The request object
            :type request: Request
            :return: Internal server error response with error message
            :rtype: JSONResponse
            """
            try:
                response = await original_route_handler(request)
            except COHERE_EXCEPTIONS as e:
                # print exception traceback to console
                logger.exception(type(e), e, e.__traceback__)
                raise HTTPException(
                    status_code=500,
                    detail=str(e),
                )
            return response

        return exception_handler
