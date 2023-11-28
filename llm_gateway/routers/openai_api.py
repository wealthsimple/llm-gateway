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

from llm_gateway.exceptions import OpenAIRouteExceptionHandler
from llm_gateway.models import (
    ChatCompletionInput,
    CompletionInput,
    EditInput,
    EmbeddingInput,
)
from llm_gateway.providers.openai import OpenAIWrapper

router = APIRouter(route_class=OpenAIRouteExceptionHandler)


@router.post("/completion")
def get_completion(user_input: CompletionInput) -> JSONResponse:
    """
    Use OpenAI's completion API to generate a response to a prompt

    :param user_input: Inputs to the OpenAI completion API, including prompt
    :type user_input: CompletionInput
    :return: Dictionary with LLM response and metadata
    :rtype: JSONResponse
    """

    wrapper = OpenAIWrapper()
    return JSONResponse(
        wrapper.send_openai_request(
            "Completion",
            "create",
            max_tokens=user_input.max_tokens,
            prompt=user_input.prompt,
            temperature=user_input.temperature,
            model=user_input.model,
            **user_input.model_kwargs
        )
    )


@router.post("/chat_completion")
def get_chat_completion(user_input: ChatCompletionInput) -> JSONResponse:
    """
    Use OpenAI's chat_completion API to generate a response given a chat (series of prompts)

    :param user_input: Inputs to the OpenAI chat_completion API, including prompt messages
    :type user_input: ChatCompletionInput
    :return: Dictionary with LLM response and metadata
    :rtype: JSONResponse
    """

    wrapper = OpenAIWrapper()
    return JSONResponse(
        wrapper.send_openai_request(
            "ChatCompletion",
            "create",
            messages=user_input.messages,
            temperature=user_input.temperature,
            model=user_input.model,
            **user_input.model_kwargs
        )
    )


@router.post("/edit")
def get_edit(user_input: EditInput) -> JSONResponse:
    """
    Use OpenAI's edit API to edit a prompt given some instruction

    :param user_input: Inputs to the OpenAI edit API, including prompt and instruction
    :type user_input: EditInput
    :return: Dictionary with edited prompts and metadata
    :rtype: JSONResponse
    """

    wrapper = OpenAIWrapper()
    return JSONResponse(
        wrapper.send_openai_request(
            "Edits",
            "create",
            prompt=user_input.prompt,
            instruction=user_input.instruction,
            model=user_input.model,
        )
    )


@router.post("/embedding")
def get_embedding(user_input: EmbeddingInput) -> JSONResponse:
    """
    Use OpenAI to turn a list of prompts into vectors

    :param user_input: Inputs to the OpenAI embedding API, including list of prompts
    :type user_input: EmbeddingInput
    :return: List of embeddings (a vector for each input prompt) and metadata
    :rtype: JSONResponse
    """

    wrapper = OpenAIWrapper()
    return JSONResponse(
        wrapper.send_openai_request(
            "Embedding",
            "create",
            embedding_texts=user_input.embedding_texts,
            model=user_input.model,
        )
    )
