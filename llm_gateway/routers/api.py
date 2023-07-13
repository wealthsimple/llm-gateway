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


from fastapi import APIRouter

from llm_gateway.routers.cohere_api import router as cohere_router
from llm_gateway.routers.openai_api import router as openai_router

"""
Main API Router
"""

api_router = APIRouter()
api_router.include_router(openai_router, prefix="/openai")
api_router.include_router(cohere_router, prefix="/cohere")


@api_router.get("/healthcheck")
async def healthcheck():
    """
    Endpoint to verify that the service is up and running
    """
    return {"message": "llm-gateway is healthy"}
