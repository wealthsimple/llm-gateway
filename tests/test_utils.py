from unittest.mock import Mock

import pytest
from llm_gateway.utils import max_retries
from openai.error import APIError


def test_retry_decorator():

    @max_retries(3)
    def normal_exception():
        raise Exception("test")

    retry_mock = Mock()

    retry_mock.side_effect = [APIError("test"), "success"]

    @max_retries(3, exceptions=[APIError])
    def openai_exception():
        result = retry_mock()
        if isinstance(result, str):
            return result
        else:
            raise result
    
    with pytest.raises(Exception):
        normal_exception()

    assert openai_exception() == "success"