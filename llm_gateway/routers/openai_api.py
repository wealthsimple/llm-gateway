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

from llm_gateway.exceptions import OpenAIRouteExceptionHandler
from llm_gateway.models import (
    ChatCompletionInput,
    CompletionInput,
    EditInput,
    EmbeddingInput,
)
from llm_gateway.providers.openai import OpenAIWrapper
from llm_gateway.utils import reraise_500

router = APIRouter(route_class=OpenAIRouteExceptionHandler)


@router.post("/completion")
@reraise_500
def get_completion(
    user_input: CompletionInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    Use OpenAI's completion API to generate a response to a prompt

    :param user_input: Inputs to the OpenAI completion API, including prompt
    :type user_input: CompletionInput
    :return: Dictionary with LLM response and metadata
    :rtype: JSONResponse
    """
    wrapper = OpenAIWrapper()
    resp, logs = wrapper.send_openai_request(
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


@router.post("/completion/stream")
@reraise_500
def get_completion_stream(
    user_input: CompletionInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    wrapper = OpenAIWrapper()

    resp, logs = wrapper.send_openai_request(
        "Completion",
        "create",
        model=user_input.model,
        max_tokens=user_input.max_tokens,
        prompt=user_input.prompt,
        temperature=user_input.temperature,
        stream=True,
        **user_input.model_kwargs,
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)

    return StreamingResponse(resp, media_type="text/plain")


@router.post("/chat_completion")
@reraise_500
def get_chat_completion(
    user_input: ChatCompletionInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    Use OpenAI's chat_completion API to generate a response given a chat (series of prompts)

    :param user_input: Inputs to the OpenAI chat_completion API, including prompt messages
    :type user_input: ChatCompletionInput
    :return: Dictionary with LLM response and metadata
    :rtype: JSONResponse
    """
    wrapper = OpenAIWrapper()
    resp, logs = wrapper.send_openai_request(
        "ChatCompletion",
        "create",
        model=user_input.model,
        messages=user_input.messages,
        temperature=user_input.temperature,
        **user_input.model_kwargs,
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return JSONResponse(resp)


@router.post("/chat_completion/stream")
@reraise_500
def get_chat_completion_stream(
    user_input: ChatCompletionInput, background_tasks: BackgroundTasks
) -> StreamingResponse:
    wrapper = OpenAIWrapper()
    response, logs = wrapper.send_openai_request(
        "ChatCompletion",
        "create",
        model=user_input.model,
        messages=user_input.messages,
        temperature=user_input.temperature,
        stream=True,
        **user_input.model_kwargs,
    )
    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return StreamingResponse(response, media_type="text/plain")


@router.post("/edit")
@reraise_500
def get_edit(user_input: EditInput, background_tasks: BackgroundTasks) -> JSONResponse:
    """
    Use OpenAI's edit API to edit a prompt given some instruction

    :param user_input: Inputs to the OpenAI edit API, including prompt and instruction
    :type user_input: EditInput
    :return: Dictionary with edited prompts and metadata
    :rtype: JSONResponse
    """
    wrapper = OpenAIWrapper()
    resp, logs = wrapper.send_openai_request(
        "Edits",
        "create",
        prompt=user_input.prompt,
        instruction=user_input.instruction,
        model=user_input.model,
    )

    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return JSONResponse(resp)


@router.post("/embedding")
@reraise_500
def get_embedding(
    user_input: EmbeddingInput, background_tasks: BackgroundTasks
) -> JSONResponse:
    """
    Use OpenAI to turn a list of prompts into vectors

    :param user_input: Inputs to the OpenAI embedding API, including list of prompts
    :type user_input: EmbeddingInput
    :return: List of embeddings (a vector for each input prompt) and metadata
    :rtype: JSONResponse
    """
    wrapper = OpenAIWrapper()
    resp, logs = wrapper.send_openai_request(
        "Embedding",
        "create",
        embedding_texts=user_input.embedding_texts,
        model=user_input.model,
    )
    background_tasks.add_task(wrapper.write_logs_to_db, db_logs=logs)
    return JSONResponse(resp)
