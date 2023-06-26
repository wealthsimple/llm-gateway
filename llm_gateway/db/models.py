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

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OpenAIRequests(Base):
    __tablename__ = "openai_requests"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_input = Column(String, nullable=True)
    user_email = Column(String, nullable=True)
    openai_response = Column(JSON, nullable=True)
    openai_model = Column(String, nullable=True)
    temperature = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False)
    openai_endpoint = Column(String, nullable=False)


class CohereRequests(Base):
    __tablename__ = "cohere_requests"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    user_input = Column(String, nullable=True)
    user_email = Column(String, nullable=True)
    cohere_response = Column(JSON, nullable=True)
    cohere_model = Column(String, nullable=True)
    temperature = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False)
    cohere_endpoint = Column(String, nullable=False)
