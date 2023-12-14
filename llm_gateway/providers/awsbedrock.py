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
from llm_gateway.exceptions import AWSBEDROCK_EXCEPTIONS
from llm_gateway.db.utils import write_record_to_db
from llm_gateway.pii_scrubber import scrub_all
from llm_gateway.utils import StreamProcessor, max_retries

settings = get_settings()


SUPPORTED_AWSBEDROCK_ENDPOINTS = {
    "Completion": ("create"),
    "Embedding": ("create"),
}

SUPPORTED_AWSBEDROCK_MODELS = [
    # AI21 Labs (Jurassic2)
    "ai21.j2-mid-v1",
    "ai21.j2-ultra-v1",
    # Amazon (Titan)
    "amazon.titan-embed-text-v1",
    "amazon.titan-text-express-v1",
    # Anthropic (Claude)
    "anthropic.claude-v1",
    "anthropic.claude-v2",
    "anthropic.claude-v2:1",
    "anthropic.claude-instant-v1",
    # Meta (Llama2)
    "meta.llama2-13b-chat-v1",
    "meta.llama2-70b-chat-v1",
]


class AWSBedrockWrapper:
    """
    This is a simple wrapper around the AWS Bedrock API client, which adds
    PII scrubbing before requests are sent, and DB logging after responses
    are received
    """

    def __init__(self) -> None:
        self._bedrock_runtime: boto3.client = self._setup_client()

    def _setup_client(self) -> boto3.client:
        """
        Setup the AWS Bedrock client with user defined credentials

        :return: The AWS Bedrock client
        """
        session_kwargs = {
            "region_name": settings.AWS_REGION,
            "profile_name": settings.AWS_PROFILE,
        }

        session = boto3.Session(**session_kwargs)

        res = session.client("sts").assume_role(
            RoleArn=settings.AWS_ROLE_ARN,
            RoleSessionName=settings.APP_NAME,
        )

        client_kwargs = {
            "aws_access_key_id": res["Credentials"]["AccessKeyId"],
            "aws_secret_access_key": res["Credentials"]["SecretAccessKey"],
            "aws_session_token": res["Credentials"]["SessionToken"],
            **session_kwargs,
        }

        bedrock_runtime = session.client(
            service_name="bedrock-runtime", config=0, **client_kwargs
        )

        return bedrock_runtime

    def _validate_awsbedrock_endpoint(
            self, 
            module: str, 
            endpoint: str, 
            model: str
        ) -> None:
        """
        Check if module, endpoint, and model are supported in AWS Bedrock, else raise an error

        :param module: The name of an AWS Bedrock module (i.e. "Completion")
        :type module: str
        :param endpoint: The name of an AWS Bedrock endpoint (i.e. "create")
        :type endpoint: str
        :param model: The name of an AWS Bedrock model (i.e. "meta.llama2-70b-chat-v1")
        :type model: str
        :raises NotImplementedError: Raised if AWS Bedrock module, endpoint, or model is not supported
        """
        if module not in SUPPORTED_AWSBEDROCK_ENDPOINTS:
            raise NotImplementedError(
                f"`awsbedrock_endpoint` must be one of `{SUPPORTED_AWSBEDROCK_ENDPOINTS.keys()}`"
            )

        if endpoint not in SUPPORTED_AWSBEDROCK_ENDPOINTS[module]:
            raise NotImplementedError(
                f"`{endpoint}` not supported action for `{module}`"
            )
        
        if model not in SUPPORTED_AWSBEDROCK_MODELS:
            raise NotImplementedError(
                f"`model` must be one of `{model}`"
            )

    @max_retries(3, exceptions=AWSBEDROCK_EXCEPTIONS)
    def _call_completion_endpoint(
        self,
        model: str,
        prompt: str,
        max_tokens: int,
        temperature: Optional[float] = 0,
        stream: bool = False,
        **kwargs,
    ) -> JSONResponse:
        """ 
        
        """
        body = {
            "prompt": prompt,
            "temperature": temperature,
            "maxTokens": max_tokens,
            **kwargs,
        }

        if stream:
            return self._bedrock_runtime.invoke_model_with_response_stream(
                modelId=model,
                body=json.dumps(body),
                contentType="application/json",
            )
            # json.loads(res["body"].read())
        
        return self._bedrock_runtime.invoke_model(
            modelId=model,
            body=json.dumps(body),
            contentType="application/json",
        )

    @max_retries(3, exceptions=AWSBEDROCK_EXCEPTIONS)
    def _call_embedding_endpoint() -> JSONResponse:
        pass

    def send_awsbedrock_request(
        self,
        awsbedrock_module: str,
        endpoint: str,
        model: str,
        max_tokens: int,
        stream: bool = False,
        prompt: Optional[str] = None,
        temperature: Optional[float] = 0,
        messages: Optional[list] = None,  # TODO: add pydantic type for messages
        instruction: Optional[str] = None,
        embedding_texts: Optional[list] = None,
        **kwargs,
    ) -> Tuple[Union[dict, Iterator[str]], dict]:
        """ """
        self._validate_awsbedrock_endpoint(awsbedrock_module, endpoint, model)

        if messages:
            messages = [scrub_all(message) for message in messages]
        if prompt:
            prompt = scrub_all(prompt)
        if embedding_texts:
            embedding_texts = [scrub_all(text) for text in embedding_texts]
        if instruction:
            instruction = scrub_all(instruction)

        if awsbedrock_module == "Completion":
            result = self._call_completion_endpoint(
                model=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream,
                **kwargs,
            )
            user_input = prompt
        elif awsbedrock_module == "Embedding":
            result = self._call_embedding_endpoint(
                model=model,
                embedding_texts=embedding_texts,
                instruction=instruction,
                **kwargs,
            )
            user_input = str(embedding_texts)

        if not stream:
            awsbedrock_response = result # *****Check what this is returning
            cached_response = awsbedrock_response
        elif awsbedrock_module == "Completion":
            stream_processor = StreamProcessor(
                stream_processor=stream_generator_awsbedrock_completion
            )
            awsbedrock_response = stream_processor.process_stream(result)
            cached_response = stream_processor.get_cached_streamed_response()
            # The cached streaming response is an empty list at this point.
            # Once the stream is returned to the user it will be populated
            # Since the DB write happens after the stream, this will always be populated

        db_record = {
            "user_input": user_input,
            "user_email": None,
            "awsbedrock_response": cached_response,
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


def stream_generator_awsbedrock_completion(generator: Iterator) -> Iterator[str]:
    """ """
    for chunk in generator:
        answer = ""
        try:
            current_response = None
            answer += current_response
        except KeyError:
            pass
        yield answer
