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

from llm_gateway.constants import AppEnv, get_settings
from llm_gateway.routers.cohere_api import router as CohereRouter
from llm_gateway.routers.openai_api import router as OpenAIRouter

settings = get_settings()

api_app = FastAPI()
api_app.include_router(OpenAIRouter, prefix="/openai")
api_app.include_router(CohereRouter, prefix="/cohere")

# allow CORS for local development with frontend
if settings.APP_ENV in (AppEnv.DEVELOPMENT, AppEnv.STAGING):
    api_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@api_app.get("/healthcheck")
async def healthcheck():
    """
    Endpoint to verify that the service is up and running
    """
    content = {"message": "llm-gateway is healthy"}
    return content
