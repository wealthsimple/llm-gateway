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

import logging
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings

level = logging.INFO
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    API_PREFIX = "/api"
    APP_TITLE = "LLM Proxy"
    APP_DESCRIPTION = "LLM Proxy Developed by Wealthsimple"

    OPENAI_API_KEY: Optional[str]
    COHERE_API_KEY: Optional[str]
    DATABASE_URL: str

    class Config:
        env_file = ".envrc"


@lru_cache()
def get_settings():
    settings = Settings()
    if not settings.OPENAI_API_KEY:
        logger.warning("Missing OPENAI_API_KEY. OpenAI features will not function.")
    if not settings.COHERE_API_KEY:
        logger.warning("Missing COHERE_API_KEY. Cohere features will not function.")

    return settings
