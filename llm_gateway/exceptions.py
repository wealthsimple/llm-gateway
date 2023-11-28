from traceback import print_exception

from cohere.error import CohereAPIError, CohereConnectionError, CohereError
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from openai.error import APIConnectionError, APIError, RateLimitError, Timeout, TryAgain

OPENAI_EXCEPTIONS = (Timeout, APIError, APIConnectionError, TryAgain, RateLimitError)
COHERE_EXCEPTIONS = (CohereError, CohereAPIError, CohereConnectionError)


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
                print_exception(type(e), e, e.__traceback__)
                response = JSONResponse(status_code=500, content={"error": str(e)})
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
                print_exception(type(e), e, e.__traceback__)
                response = JSONResponse(status_code=500, content={"error": str(e)})
            return response

        return exception_handler
