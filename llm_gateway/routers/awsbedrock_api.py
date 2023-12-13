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
    AWSBedrockCompletionInput,
    AWSBedrockEmbeddingInput,
)
from llm_gateway.providers.awsbedrock import AWSBedrockWrapper
from llm_gateway.utils import reraise_500

router = APIRouter(route_class=AWSBedrockRouteExceptionHandler)

@router.post("/completion")
@reraise_500
def get_completion(
    user_input: AWSBedrockCompletionInput, background_tasks: BackgroundTasks
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
        "Completion",
        "create",
        model=user_input.model,
        max_tokens=user_input.max_tokens,
        prompt=user_input.prompt,
        temperature=user_input.temperature,
        **user_input.model_kwargs,
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return JSONResponse(resp)

@router.post("/completion/streaming")
@reraise_500
def get_completion_stream(
    user_input: AWSBedrockCompletionInput, background_tasks: BackgroundTasks
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
        "Completion",
        "create",
        model=user_input.model,
        max_tokens=user_input.max_tokens,
        prompt=user_input.prompt,
        temperature=user_input.temperature,
        **user_input.model_kwargs,
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return StreamingResponse(resp, media_type="text/plain")


@router.post("/embedding")
@reraise_500
def get_embedding(
    user_input: AWSBedrockEmbeddingInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    Use AWS Bedrock to turn a list of prompts into vectors

    :param user_input: Inputs to the AWS Bedrock embedding API, including model and list of prompts
    :type user_input: AWSBedrockInput
    :return: List of embeddings (a vector for each input prompt) and metadata
    :rtype: JSONResponse
    """
    wrapper = AWSBedrockWrapper()
    resp, logs = wrapper.send_awsbedrock_request(
        "Embedding",
        "create",
        embedding_texts=user_input.embedding_texts,
        model=user_input.model,
    )
    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return JSONResponse(resp)
