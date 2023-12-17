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

from llm_gateway.exceptions import AWSBedrockRouteExceptionHandler
from llm_gateway.models import (
    AWSBedrockChatInput,
    AWSBedrockEmbedInput,
    AWSBedrockImageInput,
    AWSBedrockTextInput,
)
from llm_gateway.providers.awsbedrock import AWSBedrockWrapper
from llm_gateway.utils import reraise_500

router = APIRouter(route_class=AWSBedrockRouteExceptionHandler)


@router.post("/chat")
@reraise_500
def get_completion(
    user_input: AWSBedrockChatInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    Use the AWS Bedrock completion API to generate a response to a prompt

    :param user_input: Inputs to the AWS Bedrock completion API, including model and prompt
    :type user_input: AWSBedrockCompletionInput
    :return: Dictionary with LLM response and metadata
    :rtype: JSONResponse
    """
    wrapper = AWSBedrockWrapper()
    resp, logs = wrapper.send_awsbedrock_request(
        awsbedrock_module="Chat",
        model=user_input.model,
        max_tokens=user_input.max_tokens,
        messages=user_input.messages,
        temperature=user_input.temperature,
        **user_input.kwargs,
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return JSONResponse(resp)


@router.post("/chat/streaming")
@reraise_500
def get_completion_stream(
    user_input: AWSBedrockChatInput, background_tasks: BackgroundTasks
) -> StreamingResponse:
    """
    Use the AWS Bedrock completion API to generate a stream response to a prompt

    :param user_input: Inputs to the AWS Bedrock completion API, including model and prompt
    :type user_input: AWSBedrockCompletionInput
    :return: LLM response and metadata
    :rtype: StreamingResponse
    """
    wrapper = AWSBedrockWrapper()
    resp, logs = wrapper.send_awsbedrock_request(
        awsbedrock_module="Chat",
        model=user_input.model,
        max_tokens=user_input.max_tokens,
        messages=user_input.messages,
        temperature=user_input.temperature,
        **user_input.kwargs,
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return StreamingResponse(resp, media_type="text/plain")


@router.post("/text")
@reraise_500
def get_completion_stream(
    user_input: AWSBedrockTextInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    """"""
    wrapper = AWSBedrockWrapper()
    resp, logs = wrapper.send_awsbedrock_request(
        awsbedrock_module="Text",
        model=user_input.model,
        max_tokens=user_input.max_tokens,
        prompt=user_input.prompt,
        temperature=user_input.temperature,
        **user_input.kwargs,
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return JSONResponse(resp)


@router.post("/text/streaming")
@reraise_500
def get_completion_stream(
    user_input: AWSBedrockTextInput, background_tasks: BackgroundTasks
) -> StreamingResponse:
    """"""
    wrapper = AWSBedrockWrapper()
    resp, logs = wrapper.send_awsbedrock_request(
        awsbedrock_module="Text",
        model=user_input.model,
        max_tokens=user_input.max_tokens,
        prompt=user_input.prompt,
        temperature=user_input.temperature,
        **user_input.kwargs,
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return StreamingResponse(resp, media_type="text/plain")

@router.post("/embed")
@reraise_500
def get_completion_stream(
    user_input: AWSBedrockEmbedInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    """"""
    wrapper = AWSBedrockWrapper()
    resp, logs = wrapper.send_awsbedrock_request(
        awsbedrock_module="Embed",
        model=user_input.model,
        max_tokens=user_input.max_tokens,
        embedding_texts=user_input.embedding_texts,
        temperature=user_input.temperature,
        **user_input.kwargs,
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return JSONResponse(resp)


@router.post("/image")
@reraise_500
def get_completion_stream(
    user_input: AWSBedrockImageInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    """"""
    wrapper = AWSBedrockWrapper()
    resp, logs = wrapper.send_awsbedrock_request(
        awsbedrock_module="Image",
        model=user_input.model,
        max_tokens=user_input.max_tokens,
        prompt=user_input.prompt,
        temperature=user_input.temperature,
        **user_input.kwargs,
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return JSONResponse(resp)
