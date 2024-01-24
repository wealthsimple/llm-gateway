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
from starlette.responses import JSONResponse

from llm_gateway.exceptions import AWSBedrockRouteExceptionHandler
from llm_gateway.models import AWSBedrockEmbedInput, AWSBedrockTextInput
from llm_gateway.providers.awsbedrock import AWSBedrockWrapper
from llm_gateway.utils import reraise_500

router = APIRouter(route_class=AWSBedrockRouteExceptionHandler)


@router.post("/text")
@reraise_500
def get_completion_text(
    user_input: AWSBedrockTextInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    Use the AWS Bedrock API to generate a response to a prompt

    :param user_input: Inputs to the AWS Bedrock API, including prompt
    :type user_input: AWSBedrockTextInput
    :return: Dictionary with LLM response and metadata
    :rtype: JSONResponse
    """
    wrapper = AWSBedrockWrapper()
    resp, logs = wrapper.send_awsbedrock_request(
        awsbedrock_module="Text",
        model=user_input.model,
        max_tokens=user_input.max_tokens,
        prompt=user_input.prompt,
        temperature=user_input.temperature,
        **user_input.model_kwargs,
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return JSONResponse(resp)


@router.post("/embed")
@reraise_500
def get_completion_embedding(
    user_input: AWSBedrockEmbedInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    Use the AWS Bedrock API to generate a embedding vectors from a prompt

    :param user_input: Inputs to the AWS Bedrock API, including prompt
    :type user_input: AWSBedrockEmbedInput
    :return: Dictionary with LLM response and metadata
    :rtype: JSONResponse
    """
    wrapper = AWSBedrockWrapper()
    resp, logs = wrapper.send_awsbedrock_request(
        awsbedrock_module="Embed",
        model=user_input.model,
        max_tokens=user_input.max_tokens,
        embedding_texts=user_input.embedding_texts,
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return JSONResponse(resp)
