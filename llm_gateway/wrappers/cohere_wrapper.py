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
from typing import Optional

import cohere

from llm_gateway.db.models import CohereRequests
from llm_gateway.db.utils import write_record_to_db
from llm_gateway.pii_scrubber import scrub_all

SUPPORTED_COHERE_ENDPOINTS = ["generate"]


class CohereWrapper:
    """
    This is a simple wrapper around the Cohere API client, which adds
    PII scrubbing before requests are sent, and DB logging after responses
    are received
    """

    def __init__(self) -> None:
        self.cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

    def _validate_cohere_endpoint(self, endpoint: str) -> None:
        """
        Check if endpoint is a supported Cohere endpoint, else raise an error

        :param endpoint: The name of a Cohere endpoint
        :type endpoint: str
        :raises NotImplementedError: Raised if endpoint is not a supported Cohere endpoint
        """

        if endpoint not in SUPPORTED_COHERE_ENDPOINTS:
            raise NotImplementedError(
                f"Cohere endpoint must be one of `{SUPPORTED_COHERE_ENDPOINTS}`"
            )

    def _call_generate_endpoint(
        self, prompt: str, model: str, max_tokens: int, temperature: float, **kwargs
    ):
        """
        Call the generate endpoint from the Cohere client and return response

        :param prompt: String prompt
        :type prompt: str
        :param model: Model to hit
        :type model: str
        :param max_tokens: Maximum tokens for prompt and completion
        :type max_tokens: int
        :param temperature: Temperature altering the creativity of the response
        :type temperature: float
        :return: Response from Cohere
        :rtype: _type_
        """

        return self.cohere_client.generate(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )

    def _flatten_cohere_response(self, cohere_response):
        """
        Flatten response from Cohere as JSON

        :param cohere_response: Raw response from Cohere
        :type cohere_response: _type_
        :return: Flattened Cohere response as JSON
        :rtype: _type_
        """

        return json.loads(json.dumps(cohere_response, default=lambda o: o.__dict__))

    def send_cohere_request(
        self,
        endpoint: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = 0,
        **kwargs,
    ):
        """
        Send a request to the Cohere API and log interaction to the DB

        :param endpoint: Valid Cohere endpoint to hit
        :type endpoint: str
        :param model: Model to hit, defaults to None
        :type model: Optional[str], optional
        :param max_tokens: Maximum tokens for prompt and completion, defaults to None
        :type max_tokens: Optional[int], optional
        :param prompt: String prompt, defaults to None
        :type prompt: Optional[str], optional
        :param temperature: Temperature altering the creativity of the response, defaults to 0
        :type temperature: Optional[float], optional
        :return: Flattened response from Cohere
        :rtype: _type_
        """

        self._validate_cohere_endpoint(endpoint)

        # scrub sensitive information
        prompt = scrub_all(prompt)

        if endpoint == "generate":
            result = self._call_generate_endpoint(
                prompt, model, max_tokens, temperature, **kwargs
            )

        cohere_response = self._flatten_cohere_response(result)

        write_record_to_db(
            CohereRequests(
                **{
                    "user_input": prompt,
                    "user_email": None,
                    "cohere_response": cohere_response,
                    "cohere_model": model,
                    "temperature": temperature,
                    "created_at": datetime.datetime.now(),
                    "cohere_endpoint": endpoint,
                }
            )
        )
        return cohere_response
