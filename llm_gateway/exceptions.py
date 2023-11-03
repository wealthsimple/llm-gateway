from traceback import print_exception

from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from openai.error import APIConnectionError, APIError, RateLimitError, Timeout, TryAgain

OPENAI_EXCEPTIONS = (Timeout, APIError, APIConnectionError, TryAgain, RateLimitError)


class OpenAIRouteExceptionHandler(APIRoute):
    """ """

    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def exception_handler(request):
            try:
                response = await original_route_handler(request)
            except OPENAI_EXCEPTIONS as e:
                print_exception(type(e), e, e.__traceback__)
                response = JSONResponse(
                    status_code=500,
                    content={"error": e.error},
                )
            return response

        return exception_handler


# # TODO : Implement Cohere Router Exception Handler
