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

# flake8: noqa

from unittest.mock import patch

import pytest

from llm_gateway.pii_scrubber import (
    scrub_all,
    scrub_credit_card_numbers,
    scrub_dates,
    scrub_email_addresses,
    scrub_phone_numbers,
    scrub_postal_codes,
    scrub_sin_numbers,
)
from llm_gateway.providers.openai import OpenAIWrapper


@pytest.mark.parametrize(
    argnames=["test_number"],
    argvalues=[
        ("1234567890",),
        ("123-456-7890",),
        ("(123) 456-7890",),
        ("123 456 7890",),
        ("123.456.7890",),
        ("+91 (123) 456-7890",),
        ("1 (800) 555-1234",),
    ],
)
def test_scrub_phone_numbers(test_number: str):
    """Test phone number scrubbing."""

    format_str = "See you on 1980-01-02. My number is {0}. Call me at 3:04:05 PM."
    test_text = format_str.format(test_number)
    expected_text = format_str.format("[REDACTED PHONE NUMBER]")

    assert scrub_phone_numbers(test_text) == expected_text


@pytest.mark.parametrize(
    argnames=["test_number"],
    argvalues=[
        ("1234555567893333",),
        ("1234-5555-6789-3333",),
        ("1234.5555.6789.3333",),
        ("1234 5555 6789 3333",),
    ],
)
def test_scrub_credit_card_numbers(test_number: str):
    """Test credit card number scrubbing."""

    format_str = "I'd like to update my credit card. The new number is {0}."
    test_text = format_str.format(test_number)
    expected_text = format_str.format("[REDACTED CREDIT CARD NUMBER]")

    assert scrub_credit_card_numbers(test_text) == expected_text


@pytest.mark.parametrize(
    argnames=["test_number"],
    argvalues=[
        ("123456789",),
        ("123-45-6789",),
        ("123-456-789",),
        ("123 45 6789",),
        ("123 456 789",),
        ("123.45.6789",),
        ("123.456.789",),
    ],
)
def test_scrub_sin_numbers(test_number: str):
    """Test social insurance number scrubbing."""

    format_str = "I'd like to start a tax return. My TIN is {0}. I need to file by 2023-04-30 11:59:59 PM."
    test_text = format_str.format(test_number)
    expected_text = format_str.format("[REDACTED SIN NUMBER]")

    assert scrub_sin_numbers(test_text) == expected_text


@pytest.mark.parametrize(
    argnames=["test_email"],
    argvalues=[
        ("abc@def.com",),
        ("one+weird.trick@gmail.com",),
    ],
)
def test_scrub_email_addresses(test_email: str):
    """Test email address scrubbing."""

    format_str = "Does {0} look like a fake email address?"
    test_text = format_str.format(test_email)
    expected_text = format_str.format("[REDACTED EMAIL ADDRESS]")
    assert scrub_email_addresses(test_text) == expected_text


@pytest.mark.parametrize(
    argnames=["test_postal"],
    argvalues=[
        ("A1A 1A1",),
        ("A1A1A1",),
        ("A1A1a1",),
    ],
)
def test_scrub_postal_codes(test_postal: str):
    """Test postal code scrubbing."""

    format_str = "My billing address is {0}. '{0}' \"{0}\" {0}"
    test_text = format_str.format(test_postal)
    expected_text = format_str.format("[REDACTED POSTAL CODE]")
    assert scrub_postal_codes(test_text) == expected_text


@pytest.mark.parametrize(
    argnames=["test_date"],
    argvalues=[
        ("01/01/2000",),
        ("02/02/2000",),
        ("2000/03/03",),
        ("2000/04/04",),
        ("05-05-2000",),
        ("06-06-2000",),
        ("2000-07-07",),
        ("2000-08-08",),
        ("09.09.2000",),
        ("10.10.2000",),
        ("2000.11.11",),
        ("2000.12.12",),
        ("1/1/2000",),
    ],
)
def test_scrub_dates(test_date: str):
    """Test date scrubbing."""

    format_str = "My birthday is {0}."
    test_text = format_str.format(test_date)
    expected_text = format_str.format("[REDACTED DATE]")
    assert scrub_dates(test_text) == expected_text


def test_scrub_all_dict():
    """Test that scrub_all works on a dict."""

    test_dict = {"role": "user", "content": "My phone number is 123-456-7890."}
    expected_dict = {
        "role": "user",
        "content": "My phone number is [REDACTED PHONE NUMBER].",
    }

    assert scrub_all(test_dict) == expected_dict


def test_scrub_all_wrong_type():
    """Test that scrub_all does not raise any errors on non-string inputs."""

    with pytest.raises(TypeError):
        scrub_all(None)

    with pytest.raises(TypeError):
        scrub_all(123)

    with pytest.raises(TypeError):
        scrub_all(123.456)

    with pytest.raises(TypeError):
        scrub_all(True)

    with pytest.raises(TypeError):
        scrub_all(False)

    with pytest.raises(TypeError):
        scrub_all(["a", "b", "c"])


@patch("openai.ChatCompletion")
@patch("llm_gateway.providers.openai.write_record_to_db")
def test_pii_scrubber_end_to_end(mock_write_record_to_db, mock_openai_module):
    """Make a ChatGPT request with some pii and make sure it gets scrubbed."""

    class MockResponse:
        def __init__(self, resp):
            self.resp = resp

        def to_dict(self):
            return self.resp

    mock_openai_module.create.return_value = MockResponse(
        {
            "id": "chatcmpl-abc123",
            "object": "chat.completion",
            "created": 1677858242,
            "model": "gpt-3.5-turbo-0301",
            "usage": {"prompt_tokens": 13, "completion_tokens": 7, "total_tokens": 20},
            "choices": [
                {
                    "message": {"role": "assistant", "content": "\n\nThis is a test!"},
                    "finish_reason": "stop",
                    "index": 0,
                }
            ],
        }
    )  # garbage data, not important
    wrapper = OpenAIWrapper()

    result = wrapper.send_openai_request(
        "ChatCompletion",
        endpoint="create",
        messages=[
            "My phone number is 123-456-7890.",
            "My SIN is 111-222-333",
            "My credit card number is 1234-5678-9012-3456",
            "The user's email is email@123.123.123.123, AKA email@domain.ca",
            "The user's postal code is A1A 1A1, AKA a1a1A1",
            "The user's birthday is 1/1/2000",
        ],
    )

    called_with = mock_openai_module.create.call_args_list[0].kwargs["messages"]
    expected = [
        "My phone number is [REDACTED PHONE NUMBER].",
        "My SIN is [REDACTED SIN NUMBER]",
        "My credit card number is [REDACTED CREDIT CARD NUMBER]",
        "The user's email is [REDACTED EMAIL ADDRESS], AKA [REDACTED EMAIL ADDRESS]",
        "The user's postal code is [REDACTED POSTAL CODE], AKA [REDACTED POSTAL CODE]",
        "The user's birthday is [REDACTED DATE]",
    ]

    # Truncate the result. called_with contains an extra message - the mock response,
    # which isn't actually sent to OpenAI but shows up because of Python list mutability.
    assert called_with[: len(expected)] == expected
