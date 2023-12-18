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
from typing import Iterator, Optional, Tuple, Union

import boto3
from fastapi.responses import JSONResponse

from llm_gateway.constants import get_settings
from llm_gateway.db.models import AWSBedrockRequests
from llm_gateway.db.utils import write_record_to_db
from llm_gateway.exceptions import AWSBEDROCK_EXCEPTIONS
from llm_gateway.pii_scrubber import scrub_all
from llm_gateway.utils import max_retries

settings = get_settings()


SUPPORTED_AWSBEDROCK_ENDPOINTS = {
    "Text": [
        "meta.llama2-13b-chat-v1",  # ok
        "meta.llama2-70b-chat-v1",  # ok
        "ai21.j2-mid-v1",  # ok
        "ai21.j2-ultra-v1",  # ok
        "amazon.titan-text-lite-v1",  # ok
        "amazon.titan-text-express-v1",  # ok
        "anthropic.claude-v1",  # ok
        "anthropic.claude-v2",  # ok
        "anthropic.claude-v2:1",  # ok
        "anthropic.claude-instant-v1",  # ok
        "cohere.command-text-v14",  # ok
        "cohere.command-light-text-v14",  # ok
    ],
    "Embed": [
        "amazon.titan-embed-text-v1",  # ok
        "cohere.embed-english-v3",  # ok
        "cohere.embed-multilingual-v3",  # ok
    ],
}


class AWSBedrockWrapper:
    """
    This is a simple wrapper around the AWS Bedrock API client, which adds
    PII scrubbing before requests are sent, and DB logging after responses
    are received
    """

    def __init__(self) -> None:
        self._bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=settings.AWS_REGION,
        )

    def _validate_awsbedrock_endpoint(self, endpoint: str, model: str) -> None:
        """
        Check if endpoint and model are supported in AWS Bedrock, else raise an error

        :param endpoint: The name of an AWS Bedrock endpoint (i.e. "Chat")
        :type endpoint: str
        :param model: The name of an AWS Bedrock model (i.e. "meta.llama2-70b-chat-v1")
        :type model: str
        :raises NotImplementedError: Raised if AWS Bedrock module, endpoint, or model is not supported
        """
        if endpoint not in SUPPORTED_AWSBEDROCK_ENDPOINTS:
            raise NotImplementedError(
                f"`awsbedrock_endpoint` must be one of `{SUPPORTED_AWSBEDROCK_ENDPOINTS.keys()}`"
            )

        if model not in SUPPORTED_AWSBEDROCK_ENDPOINTS[endpoint]:
            raise NotImplementedError(
                f"`model` must be one of `{SUPPORTED_AWSBEDROCK_ENDPOINTS[endpoint]} for endpoint `{endpoint}`"
            )

    def _structure_model_body(
        self,
        model: str,
        max_tokens: int,
        prompt: Optional[str] = None,
        embedding_texts: Optional[list] = None,
        instruction: Optional[str] = None,
        temperature: Optional[float] = 0,
        **kwargs,
    ) -> Tuple[dict, str]:
        """
        Structure the body of the AWS Bedrock API request (Model specific)

        :param model: The name of an AWS Bedrock model (i.e. "meta.llama2-70b-chat-v1")
        :type model: str
        :param max_tokens: The maximum number of tokens to generate
        :type max_tokens: int
        :param prompt: String prompt, defaults to None
        :type prompt: Optional[str]
        :param embedding_texts: List of prompts, defaults to None
        :type embedding_texts: Optional[list]
        :param instruction: Instructions for model, defaults to None
        :type instruction: Optional[str]
        :param temperature: The temperature of the model, defaults to 0
        :type temperature: Optional[float]
        :param kwargs: other model-specific parameters to pass to AWS Bedrock. (ie- topP, stop_sequences, seed, etc.)
        :type kwargs: Optional[dict]
        :return: Body of the model-specific request to the AWS Bedrock API and the strigified user input
        :rtype: Tuple[dict, str]
        """

        match model:
            case "ai21.j2-mid-v1" | "ai21.j2-ultra-v1":
                return (
                    {
                        "prompt": prompt,
                        "maxTokens": max_tokens,
                        "temperature": temperature,
                        **kwargs,
                    },
                    prompt,
                )
            case "amazon.titan-text-lite-v1" | "amazon.titan-text-express-v1":
                return (
                    {
                        "inputText": prompt,
                        "textGenerationConfig": {
                            "maxTokenCount": max_tokens,
                            "temperature": temperature,
                            **kwargs,
                        },
                    },
                    prompt,
                )
            case "amazon.titan-embed-text-v1":
                return (
                    {
                        "inputText": f"{embedding_texts}",
                    },
                    f"{embedding_texts}",
                )
            case "anthropic.claude-v1" | "anthropic.claude-v2" | "anthropic.claude-v2:1" | "anthropic.claude-instant-v1":
                return (
                    {
                        "prompt": f"\n\nHuman: {prompt}\n\nAssistant: {instruction}",
                        "max_tokens_to_sample": max_tokens,
                        "temperature": temperature,
                        **kwargs,
                    },
                    prompt,
                )
            case "cohere.command-text-v14" | "cohere.command-light-text-v14":
                return (
                    {
                        "prompt": prompt,
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        **kwargs,
                    },
                    prompt,
                )
            case "cohere.embed-english-v3" | "cohere.embed-multilingual-v3":
                return (
                    {"texts": embedding_texts, "input_type": "search_document"},
                    f"{embedding_texts}",
                )
            case "meta.llama2-13b-chat-v1" | "meta.llama2-70b-chat-v1":
                return (
                    {
                        "prompt": f"[INST]{instruction}[/INST]\n {prompt}",
                        "max_gen_len": max_tokens,
                        "temperature": temperature,
                        **kwargs,
                    },
                    f"[INST]{instruction}[/INST]\n {prompt}",
                )

    @max_retries(3, exceptions=AWSBEDROCK_EXCEPTIONS)
    def _invoke_awsbedrock_model(
        self,
        model: str,
        body: dict,
    ) -> JSONResponse:
        """ """

        res = self._bedrock_runtime.invoke_model(
            modelId=model,
            contentType="application/json",
            accept="*/*",
            body=json.dumps(body),
        )

        return json.loads(res.get("body").read())

    def send_awsbedrock_request(
        self,
        awsbedrock_module: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = 0,
        instruction: Optional[str] = None,
        embedding_texts: Optional[str] = None,
        **kwargs,
    ) -> Tuple[Union[dict, Iterator[str]], dict]:
        """
        Send a request to the AWS Bedrock API and return response and logs for db write

        :param openai_module: Valid AWS Bedrock module to hit (i.e. "Chat")
        :type openai_module: str
        :param model: Model to hit, defaults to None
        :type model: Optional[str]
        :param max_tokens: Maximum tokens for prompt and completion, defaults to None
        :type max_tokens: Optional[int]
        :param prompt: _description_, defaults to None
        :type prompt: String prompt, if calling completion or edits, optional
        :param temperature: Temperature altering the creativity of the response, defaults to 0
        :type temperature: Optional[float]
        :param instruction: How to perform edits, if calling edits, defaults to None
        :type instruction: Optional[str]
        :param embedding_texts: List of prompts, if calling embedding, defaults to None
        :type embedding_texts: Optional[list]
        :param kwargs: other parameters to pass to openai api. (ie- functions, function_call, etc.)
        :type kwargs: Optional[dict]
        :return: Flattened response from OpenAI
        :rtype: _type_
        """
        self._validate_awsbedrock_endpoint(endpoint=awsbedrock_module, model=model)

        if prompt:
            prompt = scrub_all(prompt)
        if embedding_texts:
            embedding_texts = [scrub_all(text) for text in embedding_texts]
        if instruction:
            instruction = scrub_all(instruction)

        body, user_input = self._structure_model_body(
            model=model,
            prompt=prompt,
            embedding_texts=embedding_texts,
            instruction=instruction,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )

        awsbedrock_response = self._invoke_awsbedrock_model(model, body)

        db_record = {
            "user_input": user_input,
            "user_email": None,
            "awsbedrock_response": awsbedrock_response,
            "awsbedrock_model": model,
            "temperature": temperature,
            "extras": json.dumps(kwargs),
            "awsbedrock_endpoint": awsbedrock_module,
            "created_at": datetime.datetime.now(),
        }

        return awsbedrock_response, db_record

    def write_logs_to_db(self, db_logs: dict):
        """ """
        if isinstance(db_logs["awsbedrock_response"], list):
            db_logs["awsbedrock_response"] = "".join(db_logs["awsbedrock_response"])
        write_record_to_db(AWSBedrockRequests(**db_logs))
