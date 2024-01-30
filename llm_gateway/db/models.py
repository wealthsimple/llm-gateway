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

import enum

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Provider(enum.StrEnum):
    OPENAI = "openai_requests"
    COHERE = "cohere_requests"
    AWSBEDROCK = "awsbedrock_requests"


class CommonRequest(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_input = Column(String, nullable=True)
    user_email = Column(String, index=True, nullable=True)
    temperature = Column(Float, nullable=True)
    created_at = Column(DateTime, index=True, nullable=False)
    extras = Column(JSON, nullable=True)


class OpenAIRequests(CommonRequest):
    __tablename__ = Provider.OPENAI
    openai_response = Column(JSON, nullable=True)
    openai_model = Column(String, nullable=True)
    openai_endpoint = Column(String, nullable=False)


class CohereRequests(CommonRequest):
    __tablename__ = Provider.COHERE
    cohere_response = Column(JSON, nullable=True)
    cohere_model = Column(String, nullable=True)
    cohere_endpoint = Column(String, nullable=False)


class AWSBedrockRequests(CommonRequest):
    __tablename__ = Provider.AWSBEDROCK
    awsbedrock_response = Column(JSON, nullable=True)
    awsbedrock_model = Column(String, nullable=True)
    awsbedrock_endpoint = Column(String, nullable=False)
