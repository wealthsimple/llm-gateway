from unittest.mock import Mock

import pytest
from llm_gateway.utils import max_retries
from openai.error import APIError


def test_retry_decorator_mismatch_exception():
    retry_mock = Mock()
    retry_mock.side_effect = [APIError("test"), "success"]

    @max_retries(1, exceptions=(ValueError,))
    def mismatch_exception():
        return retry_mock()
    
    with pytest.raises(APIError):
        mismatch_exception()


def test_retry_decorator_matching_exception():
    retry_mock = Mock()
    retry_mock.side_effect = [APIError("test"), "success"]

    ## Matching retry exception
    @max_retries(1, exceptions=(APIError,))
    def matching_exception():
        return retry_mock()

    assert matching_exception() == "success"