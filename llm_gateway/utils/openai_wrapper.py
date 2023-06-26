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


import datetime
import json
import os
from typing import List, Optional

import openai

from llm_gateway.db.models import OpenAIRequests
from llm_gateway.db.utils import write_record_to_db
from llm_gateway.pii_scrubber import scrub_all

SUPPORTED_OPENAI_ENDPOINTS = {
    "Model": ["list", "retrieve"],
    "ChatCompletion": ["create"],
    "Completion": ["create"],
    "Edits": ["create"],
    "Embedding": ["create"],
}


class OpenAIWrapper:
    """
    This is a simple wrapper around the OpenAI API client, which adds
    PII scrubbing before requests are sent, and DB logging after responses
    are received
    """

    def __init__(self) -> None:
        if not openai.api_key:
            openai.api_key = os.getenv("OPENAI_API_KEY")

    def _validate_openai_endpoint(self, module: str, endpoint: str) -> None:
        """
        Check if module and endpoint are supported in OpenAI, else raise an error

        :param module: The name of an OpenAI module (i.e. "Completion")
        :type module: str
        :param endpoint: The name of an OpenAI endpoint (i.e. "create")
        :type endpoint: str
        :raises NotImplementedError: Raised if OpenAI module or endpoint is not supported
        """

        if module not in SUPPORTED_OPENAI_ENDPOINTS:
            raise NotImplementedError(
                f"`openai_endpoint` must be one of `{SUPPORTED_OPENAI_ENDPOINTS.keys()}`"
            )

        if endpoint not in SUPPORTED_OPENAI_ENDPOINTS[module]:
            raise NotImplementedError(
                f"`{endpoint}` not supported action for `{module}`"
            )

    def _call_model_endpoint(self, endpoint: str, model: Optional[str] = None):
        """
        List or retrieve model(s) from OpenAI

        :param endpoint: Whether to "list" models or "retrieve" a model
        :type endpoint: str
        :param model: Name of model, if "retrieve" is passed, defaults to None
        :type model: Optional[str], optional
        :raises Exception: Raised if endpoint is "retrieve" and model is unspecified
        :return: List of models or retrieved model
        :rtype: _type_
        """

        if endpoint == "list":
            return openai.Model.list()
        elif endpoint == "retrieve":
            if not model:
                raise Exception("retrieve model needs model name as input")
            return openai.Model.retrieve(model)

    def _call_completion_endpoint(
        self, prompt: str, model: str, max_tokens: int, temperature: float, **kwargs
    ):
        """
        Call the completion endpoint from the OpenAI client and return response

        :param prompt: String prompt
        :type prompt: str
        :param model: Model to hit
        :type model: str
        :param max_tokens: Maximum tokens for prompt and completion
        :type max_tokens: int
        :param temperature: Temperature altering the creativity of the response
        :type temperature: float
        :return: Response from OpenAI
        :rtype: _type_
        """

        return openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )

    def _call_chat_completion_endpoint(
        self, model: str, messages: list, temperature: float = 0
    ):
        """
        Call the chat completion endpoint from the OpenAI client and return response

        :param model: Model to hit
        :type model: str
        :param messages: List of messages in the chat so far
        :type messages: list
        :param temperature: Temperature altering the creativity of the response, defaults to 0
        :type temperature: float, optional
        :return: Response from OpenAI
        :rtype: _type_
        """

        return openai.ChatCompletion.create(
            model=model, messages=messages, temperature=temperature
        )

    def _call_edits_endpoint(self, model: str, input: str, instruction: str):
        """
        Call the edits endpoint from the OpenAI client and return response

        :param model: Model to hit
        :type model: str
        :param input: String to perform the edit on
        :type input: str
        :param instruction: How to edit the input string
        :type instruction: str
        :return: Response from OpenAI containing edited input
        :rtype: _type_
        """

        return openai.Edit.create(model=model, input=input, instruction=instruction)

    def _call_embedding_endpoint(self, model: str, texts: List[str]):
        """
        Call the embedding endpoint from the OpenAI client and return response

        :param model: Model to hit
        :type model: str
        :param texts: List of strings to embed
        :type texts: List[str]
        :return: Response from OpenAI containing embeddedings
        :rtype: _type_
        """

        return openai.Embedding.create(input=texts, model=model)

    def _flatten_openai_response(self, openai_response):
        """
        Flatten response from OpenAI as JSON

        :param openai_response: Raw response from OpenAI
        :type openai_response: _type_
        :return: Flattened OpenAI response as JSON
        :rtype: _type_
        """

        return json.loads(json.dumps(openai_response, default=lambda o: o.__dict__))

    def send_openai_request(
        self,
        openai_module: str,
        endpoint: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = 0,
        messages: Optional[list] = None,  # TODO: add pydantic type for messages
        instruction: Optional[str] = None,
        embedding_texts: Optional[list] = None,
        **kwargs,
    ):
        """
        Send a request to the OpenAI API and log interactions to the DB

        :param openai_module: Valid OpenAI module to hit (i.e. "Completion")
        :type openai_module: str
        :param endpoint: Valid OpenAI endpoint to hit (i.e. "create")
        :type endpoint: str
        :param model: Model to hit, defaults to None
        :type model: Optional[str], optional
        :param max_tokens: Maximum tokens for prompt and completion, defaults to None
        :type max_tokens: Optional[int], optional
        :param prompt: _description_, defaults to None
        :type prompt: String prompt, if calling completion or edits, optional
        :param temperature: Temperature altering the creativity of the response, defaults to 0
        :type temperature: Optional[float], optional
        :param messages: List of prior messages, if calling chat completion, defaults to None
        :type messages: Optional[list], optional
        :param instruction: How to perform edits, if calling edits, defaults to None
        :type instruction: Optional[str], optional
        :param embedding_texts: List of prompts, if calling embedding, defaults to None
        :type embedding_texts: Optional[list], optional
        :return: Flattened response from OpenAI
        :rtype: _type_
        """

        self._validate_openai_endpoint(openai_module, endpoint)

        # scrub sensitive information
        if messages:
            messages = [scrub_all(message) for message in messages]
        if prompt:
            prompt = scrub_all(prompt)
        if embedding_texts:
            embedding_texts = [scrub_all(text) for text in embedding_texts]
        if instruction:
            instruction = scrub_all(instruction)

        if openai_module == "Model":
            result = self._call_model_endpoint(endpoint, model)
            user_input = f"/Model/{endpoint}"
        elif openai_module == "Completion":
            result = self._call_completion_endpoint(
                prompt, model, max_tokens, temperature, **kwargs
            )
            user_input = prompt
        elif openai_module == "ChatCompletion":
            result = self._call_chat_completion_endpoint(model, messages, temperature)
            messages.append(
                {
                    "user": "assistant",
                    "content": result["choices"][0]["message"]["content"],
                }
            )
            user_input = str(messages)
        elif openai_module == "Edits":
            result = self._call_edits_endpoint(model, prompt, instruction)
            user_input = f"instruction: {instruction} ON prompt: {prompt}"
        elif openai_module == "Embedding":
            result = self._call_embedding_endpoint(model, embedding_texts)
            user_input = str(embedding_texts)

        openai_response = self._flatten_openai_response(result)

        write_record_to_db(
            OpenAIRequests(
                **{
                    "user_input": user_input,
                    "user_email": None,
                    "openai_response": openai_response,
                    "openai_model": model,
                    "temperature": temperature,
                    "openai_endpoint": openai_module,
                    "created_at": datetime.datetime.now(),
                }
            )
        )
        return openai_response
