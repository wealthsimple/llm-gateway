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
from typing import Any, Dict, List, Optional, Tuple

import boto3

from llm_gateway.constants import get_settings
from llm_gateway.db.models import AWSBedrockRequests
from llm_gateway.db.utils import write_record_to_db
from llm_gateway.exceptions import AWSBEDROCK_EXCEPTIONS
from llm_gateway.pii_scrubber import scrub_all
from llm_gateway.types import AWSBedrockResponse, DBRecord
from llm_gateway.utils import max_retries

settings = get_settings()


META_LLAMA2_13B_CHAT_V1 = "meta.llama2-13b-chat-v1"
META_LLAMA2_70B_CHAT_V1 = "meta.llama2-70b-chat-v1"
AI21_J2_MID_V1 = "ai21.j2-mid-v1"
AI21_J2_ULTRA_V1 = "ai21.j2-ultra-v1"
AMAZON_TITAN_TEXT_LITE_V1 = "amazon.titan-text-lite-v1"
AMAZON_TITAN_TEXT_EXPRESS_V1 = "amazon.titan-text-express-v1"
ANTHROPIC_CLAUDE_V1 = "anthropic.claude-v1"
ANTHROPIC_CLAUDE_V2 = "anthropic.claude-v2"
ANTHROPIC_CLAUDE_V2_1 = "anthropic.claude-v2:1"
ANTHROPIC_CLAUDE_INSTANT_V1 = "anthropic.claude-instant-v1"
COHERE_COMMAND_TEXT_V14 = "cohere.command-text-v14"
COHERE_COMMAND_LIGHT_TEXT_V14 = "cohere.command-light-text-v14"
AMAZON_TITAN_EMBED_TEXT_V1 = "amazon.titan-embed-text-v1"
COHERE_EMBED_ENGLISH_V3 = "cohere.embed-english-v3"
COHERE_EMBED_MULTILINGUAL_V3 = "cohere.embed-multilingual-v3"


SUPPORTED_AWSBEDROCK_ENDPOINTS = {
    "Text": [
        META_LLAMA2_13B_CHAT_V1,
        META_LLAMA2_70B_CHAT_V1,
        AI21_J2_MID_V1,
        AI21_J2_ULTRA_V1,
        AMAZON_TITAN_TEXT_LITE_V1,
        AMAZON_TITAN_TEXT_EXPRESS_V1,
        ANTHROPIC_CLAUDE_V1,
        ANTHROPIC_CLAUDE_V2,
        ANTHROPIC_CLAUDE_V2_1,
        ANTHROPIC_CLAUDE_INSTANT_V1,
        COHERE_COMMAND_TEXT_V14,
        COHERE_COMMAND_LIGHT_TEXT_V14,
    ],
    # Embedding endpoints are only supportred in the backend API
    "Embed": [
        AMAZON_TITAN_EMBED_TEXT_V1,
        COHERE_EMBED_ENGLISH_V3,
        COHERE_EMBED_MULTILINGUAL_V3,
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
            aws_access_key_id=settings.AWS_PUBLIC_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_PRIVATE_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            service_name="bedrock-runtime",
        )

    def _validate_awsbedrock_endpoint(self, endpoint: str, model: str) -> None:
        """
        Check if endpoint and model are supported in AWS Bedrock, else raise an error

        :param endpoint: The name of an AWS Bedrock endpoint (i.e. "Text")
        :type endpoint: str
        :param model: The name of an AWS Bedrock model (i.e. "anthropic.claude-v2:1")
        :type model: str
        :raises NotImplementedError: Raised if AWS Bedrock module, endpoint, or model is not supported
        """
        if endpoint not in SUPPORTED_AWSBEDROCK_ENDPOINTS:
            raise NotImplementedError(
                f"`awsbedrock_endpoint` must be one of `{SUPPORTED_AWSBEDROCK_ENDPOINTS.keys()}`"
            )

        if model not in SUPPORTED_AWSBEDROCK_ENDPOINTS[endpoint]:
            raise NotImplementedError(
                f"`model` must be one of `{SUPPORTED_AWSBEDROCK_ENDPOINTS[endpoint]} for endpoint `{endpoint}`"  # noqa
            )

    def _structure_model_body(
        self,
        model: str,
        max_tokens: int,
        prompt: Optional[str] = None,
        embedding_texts: Optional[List[str]] = None,
        instruction: Optional[str] = None,
        temperature: Optional[float] = 0,
        **kwargs: Any,
    ) -> Tuple[Dict[str, Any], str]:
        """
        Structure the body of the AWS Bedrock API request (Model specific)

        :param model: The name of an AWS Bedrock model (i.e. "anthropic.claude-v2:1")
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
        :param kwargs: other model-specific parameters to pass to AWS Bedrock.
            (ie- topP, stop_sequences, seed, etc.)
        :type kwargs: Optional[dict]
        :return: Body of the model-specific request to the AWS Bedrock API and the strigified user input
        :rtype: Tuple[dict, str]
        """

        if model in (AI21_J2_MID_V1, AI21_J2_ULTRA_V1):
            return (
                {
                    "prompt": prompt,
                    "maxTokens": max_tokens,
                    "temperature": temperature,
                    **kwargs,
                },
                prompt,
            )
        if model in (AMAZON_TITAN_TEXT_LITE_V1, AMAZON_TITAN_TEXT_EXPRESS_V1):
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
        if model in (AMAZON_TITAN_EMBED_TEXT_V1,):
            return (
                {
                    "inputText": f"{embedding_texts}",
                },
                f"{embedding_texts}",
            )
        if model in (
            ANTHROPIC_CLAUDE_V1,
            ANTHROPIC_CLAUDE_V2,
            ANTHROPIC_CLAUDE_V2_1,
            ANTHROPIC_CLAUDE_INSTANT_V1,
        ):
            return (
                {
                    "prompt": f"\n\nHuman: {prompt} \n\nAssistant:",
                    "max_tokens_to_sample": max_tokens,
                    "temperature": temperature,
                    **kwargs,
                },
                prompt,
            )
        if model in (COHERE_COMMAND_TEXT_V14, COHERE_COMMAND_LIGHT_TEXT_V14):
            return (
                {
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    **kwargs,
                },
                prompt,
            )
        if model in (COHERE_EMBED_ENGLISH_V3, COHERE_EMBED_MULTILINGUAL_V3):
            return (
                {"texts": embedding_texts, "input_type": "search_document"},
                f"{embedding_texts}",
            )
        if model in (META_LLAMA2_13B_CHAT_V1, META_LLAMA2_70B_CHAT_V1):
            return (
                {
                    "prompt": prompt,
                    "max_gen_len": max_tokens,
                    "temperature": temperature,
                    **kwargs,
                },
                f"[INST]{instruction}[/INST]\n {prompt}",
            )

        # If no model is matched, raise NotImplementedError
        raise NotImplementedError(
            f"{model}` is not supported by the AWS Bedrock API. Please choose one of `{SUPPORTED_AWSBEDROCK_ENDPOINTS}"  # noqa
        )

    @max_retries(3, exceptions=AWSBEDROCK_EXCEPTIONS)
    def _invoke_awsbedrock_model(
        self,
        model: str,
        body: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Call the invoke model enpoint from the AWS Bedrock client and return response

        :param model: The name of an AWS Bedrock model (i.e. "anthropic.claude-v2:1")
        :type model: str
        :param body: Body of the model-specific request to the AWS Bedrock API
        :type body: dict
        :return: Response from the AWS Bedrock API
        :rtype: JSONResponse
        """

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
        model: str,
        max_tokens: Optional[int] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = 0,
        instruction: Optional[str] = None,
        embedding_texts: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Tuple[AWSBedrockResponse, DBRecord]:
        """
        Send a request to the AWS Bedrock API and return response and logs for db write

        :param awsbedrock_module: Valid AWS Bedrock module to hit (i.e. "Text")
        :type awsbedrock_module: str
        :param model: Model to hit
        :type model: str
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
        :param kwargs: other model-specific parameters to pass to AWS Bedrock.
            (ie- topP, stop_sequences, seed, etc.)
        :type kwargs: Optional[dict]
        :return: Flattened response from AWS Bedrock API and logs for db write
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

    def write_logs_to_db(self, db_logs: Dict[str, Any]) -> None:
        if isinstance(db_logs["awsbedrock_response"], list):
            db_logs["awsbedrock_response"] = "".join(db_logs["awsbedrock_response"])
        write_record_to_db(AWSBedrockRequests(**db_logs))
