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

import json

import boto3

from llm_gateway.constants import get_settings

settings = get_settings()

SUPPORTED_AWSBEDROCK_ENDPOINTS = {
    "": ("", ""),
    "": "",
}


class AWSBedrockWrapper:
    """ """

    def __init__(self) -> None:
        self._bedrock_runtime = self._setup_client()

    def _setup_client(self) -> boto3.client:
        """
        Setup the AWS Bedrock client with the appropriate credentials


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
            **session_kwargs,
            "aws_access_key_id": res["Credentials"]["AccessKeyId"],
            "aws_secret_access_key": res["Credentials"]["SecretAccessKey"],
            "aws_session_token": res["Credentials"]["SessionToken"],
        }

        bedrock_runtime = session.client(
            service_name="bedrock-runtime", config=0, **client_kwargs
        )

        return bedrock_runtime

    def _validate_awsbedrock_endpoint(self, module: str, endpoint: str) -> None:
        """
        Check if module and endpoint are supported in AWS Bedrock, else raise an error

        :param module: The name of an OpenAI module (i.e. "Completion")
        :type module: str
        :param endpoint: The name of an OpenAI endpoint (i.e. "create")
        :type endpoint: str
        :raises NotImplementedError: Raised if OpenAI module or endpoint is not supported
        """
        if module not in SUPPORTED_AWSBEDROCK_ENDPOINTS:
            raise NotImplementedError(
                f"`awsbedrock_endpoint` must be one of `{SUPPORTED_AWSBEDROCK_ENDPOINTS.keys()}`"
            )

        if endpoint not in SUPPORTED_AWSBEDROCK_ENDPOINTS[module]:
            raise NotImplementedError(
                f"`{endpoint}` not supported action for `{module}`"
            )

    def send_awsbedrock_request(self):
        """ """
        pass
