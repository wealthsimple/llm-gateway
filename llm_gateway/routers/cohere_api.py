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

from fastapi import APIRouter
from starlette.responses import JSONResponse

from llm_gateway.exceptions import CohereRouteExceptionHandler
from llm_gateway.models import GenerateInput
from llm_gateway.providers.cohere import CohereWrapper

router = APIRouter(route_class=CohereRouteExceptionHandler)


@router.post("/generate")
def generate(user_input: GenerateInput) -> JSONResponse:
    """
    Use Cohere's API to generate a response to a prompt

    :param user_input: Inputs to the Cohere API, including prompt
    :type user_input: GenerateInput
    :return: Dictionary with LLM response and metadata
    :rtype: JSONResponse
    """

    wrapper = CohereWrapper()
    return JSONResponse(
        wrapper.send_cohere_request(
            "generate",
            max_tokens=user_input.max_tokens,
            prompt=user_input.prompt,
            temperature=user_input.temperature,
            model=user_input.model,
        )
    )
