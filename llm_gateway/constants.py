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

from enum import StrEnum
from functools import lru_cache
from pathlib import Path
from typing import Optional

import pkg_resources
from pydantic import BaseSettings, Field

import llm_gateway


class AppEnv(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    # General Constants
    API_PREFIX = "/api"
    APP_NAME: str = Field(default="llm-gateway")
    APP_ENV: AppEnv = Field(default="development")
    APP_VERSION: str = Field(default="snapshot")
    APP_TITLE: str = "LLM Gateway"
    APP_DESCRIPTION: str = (
        "A proxy service in front of llm models to encourage the responsible use of AI"
    )

    # API Keys
    OPENAI_API_KEY: Optional[str]
    COHERE_API_KEY: Optional[str]

    # AWS Client Keys
    AWS_REGION: Optional[str]
    AWS_PROFILE: Optional[str]
    AWS_ROLE_ARN: Optional[str]

    # Postgres Database
    DATABASE_URL: str

    MODULE_PATH = Path(
        pkg_resources.resource_filename(llm_gateway.__name__, "")
    ).absolute()

    class Config:
        env_file = ".envrc"


@lru_cache()
def get_settings():
    settings = Settings()
    return settings
