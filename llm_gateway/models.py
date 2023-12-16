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

from typing import List

from pydantic import BaseModel


class GenerateInput(BaseModel):
    temperature: float
    prompt: str
    max_tokens: int = 50
    model: str = "command-light"
    model_kwargs: dict = {}


class SummarizeInput(BaseModel):
    temperature: float
    prompt: str
    additional_command: str = ""
    model: str = "command-light"
    model_kwargs: dict = {}


class CompletionInput(BaseModel):
    model: str = "text-davinci-003"
    prompt: str
    max_tokens: int = 50
    temperature: float = 0
    model_kwargs: dict = {}


class ChatCompletionInput(BaseModel):
    model: str = "gpt-3.5-turbo"
    messages: list = [
        {"role": "assistant", "content": "You are an intelligent assistant."}
    ]
    temperature: float = 0
    max_tokens: int = 2000
    model_kwargs: dict = {}


class EditInput(BaseModel):
    prompt: str
    instruction: str
    model: str = "text-davinci-edit-001"


class EmbeddingInput(BaseModel):
    embedding_texts: List[str]
    model: str = "text-embedding-ada-002"


class AWSBedrockInput(BaseModel):
    model: str
    max_tokens: int
    prompt: str
    temperature: float = 0
    model_kwargs: dict = {}


class AmazonTitanCompletionInput(AWSBedrockInput):
    model: str = ""
    max_tokens: int
    prompt: str
    temperature: float = 0
    model_kwargs: dict = {}
