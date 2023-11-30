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

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import StreamingResponse
from starlette.responses import JSONResponse

from llm_gateway.exceptions import CohereRouteExceptionHandler
from llm_gateway.models import GenerateInput, SummarizeInput
from llm_gateway.providers.cohere import CohereWrapper
from llm_gateway.utils import reraise_500

router = APIRouter(route_class=CohereRouteExceptionHandler)


@router.post("/generate")
@reraise_500
def generate(
    user_input: GenerateInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    Use Cohere's API to generate a response to a prompt

    :param user_input: Inputs to the Cohere API, including prompt
    :type user_input: GenerateInput
    :return: Dictionary with LLM response and metadata
    :rtype: JSONResponse
    """
    wrapper = CohereWrapper()
    resp, logs = wrapper.send_cohere_request(
        "generate",
        max_tokens=user_input.max_tokens,
        prompt=user_input.prompt,
        temperature=user_input.temperature,
        model=user_input.model,
        **user_input.model_kwargs
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return JSONResponse(resp)


@router.post("/generate/stream")
@reraise_500
def generate_stream(
    user_input: GenerateInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    wrapper = CohereWrapper()

    response, logs = wrapper.send_cohere_request(
        "generate",
        max_tokens=user_input.max_tokens,
        prompt=user_input.prompt,
        temperature=user_input.temperature,
        model=user_input.model,
        stream=True,
        **user_input.model_kwargs
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)

    return StreamingResponse(response, media_type="text/plain")


@router.post("/summarize")
@reraise_500
def summarize(
    user_input: SummarizeInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    Use Cohere's API to summarize a response to a prompt based on additional_command

    :param user_input: Inputs to the Cohere API, including prompt
    :type user_input: SummarizeInput
    :return: Dictionary with LLM response and metadata
    :rtype: JSONResponse
    """
    wrapper = CohereWrapper()
    resp, logs = wrapper.send_cohere_request(
        "summarize",
        prompt=user_input.prompt,
        additional_command=user_input.additional_command,
        temperature=user_input.temperature,
        model=user_input.model,
        **user_input.model_kwargs
    )
    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return resp
