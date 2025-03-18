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
import re


def scrub_all(text: str | dict) -> str | dict:
    """
    Scrub all PII in text

    :param text: Input to be scrubbed of PII
    :type text: str | dict
    :raises TypeError: Invalid input type entered
    :return: Input text after being scrubbed of PII
    :rtype: str | dict
    """

    if isinstance(text, dict):
        # scrub content val in dict
        return text | {"content": scrub_all(text["content"])}
    elif not isinstance(text, str):
        raise TypeError(f"Expected str/dict, got {type(text)=}")

    for scrubber in ALL_SCRUBBERS:
        text = scrubber(text)

    return text


def scrub_phone_numbers(text: str) -> str:
    """
    Scrub phone numbers in text, adapted from: https://stackoverflow.com/a/16699507

    :param text: Input text to scrub
    :type text: str
    :return: Input text with any phone numbers scrubbed
    :rtype: str
    """

    return re.sub(
        r"(\+?\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",
        "[REDACTED PHONE NUMBER]",
        text,
    )


def scrub_credit_card_numbers(text: str) -> str:
    """
    Scrub credit card numbers in text

    :param text: Input text to scrub
    :type text: str
    :return: Input text with any credit card numbers scrubbed
    :rtype: str
    """

    return re.sub(
        r"\b(?:\d[ -\.]*?){13,16}\b",
        "[REDACTED CREDIT CARD NUMBER]",
        text,
    )


def scrub_sin_numbers(text: str) -> str:
    """
    Scrub SIN numbers in text

    :param text: Input text to scrub
    :type text: str
    :return: Input text with any SIN numbers scrubbed
    :rtype: str
    """

    return re.sub(
        r"\b(?:\d[ -\.]*?){9}\b",
        "[REDACTED SIN NUMBER]",
        text,
    )


def scrub_email_addresses(text: str) -> str:
    """
    Scrub email addresses in text, adapted from: https://stackoverflow.com/a/201378

    :param text: Input text to scrub
    :type text: str
    :return: Input text with any email addresses scrubbed
    :rtype: str
    """

    return re.sub(
        "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
        "[REDACTED EMAIL ADDRESS]",
        text,
    )


def scrub_postal_codes(text: str) -> str:
    """
    Scrub postal codes in text

    :param text: Input text to scrub
    :type text: str
    :return: Input text with any postal codes scrubbed
    :rtype: str
    """

    return re.sub(
        r"\b[A-Za-z][0-9][A-Za-z] ?[0-9][A-Za-z][0-9]\b",
        "[REDACTED POSTAL CODE]",
        text,
    )


def scrub_dates(text: str) -> str:
    """
    Scrub dates in text

    :param text: Input text to scrub
    :type text: str
    :return: Input text with any datess scrubbed
    :rtype: str
    """
    return re.sub(
        r"\b(?:\d{1,2}[-/.]\d{1,2}[-/.]\d{4}|\d{4}[-/.]\d{1,2}[-/.]\d{1,2})\b",
        "[REDACTED DATE]",
        text,
    )


ALL_SCRUBBERS = [
    scrub_phone_numbers,
    scrub_credit_card_numbers,
    scrub_email_addresses,
    scrub_postal_codes,
    scrub_dates,
    # move sin scrubber to the end since it's over-eager
    scrub_sin_numbers,
]
