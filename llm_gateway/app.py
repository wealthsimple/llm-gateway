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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from llm_gateway.routers import cohere_api, openai_api

app = FastAPI()
app.title = "LLM Proxy"
app.description = "LLM Proxy Developed by Wealthsimple"


api = FastAPI(openapi_prefix="/api")
api.include_router(openai_api.router, prefix="/openai")
api.include_router(cohere_api.router, prefix="/cohere")

app.mount("/api", api, name="api")

# Allow Front-end Origin in local development
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/healthcheck")
async def healthcheck():
    """
    Endpoint to verify that the service is up and running
    """
    return {"message": "llm-gateway is healthy"}
