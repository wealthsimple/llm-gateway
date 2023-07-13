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

from llm_gateway.config import get_settings
from llm_gateway.routers.api import api_router

settings = get_settings()


def create_bare_app():
    app = FastAPI(title=settings.APP_TITLE)
    app.description = settings.APP_DESCRIPTION
    return app


def attach_cors_middleware(app: FastAPI) -> FastAPI:
    # Allow Front-end Origin in local development
    origins = ["http://localhost:3000"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def attach_api_routes(app: FastAPI) -> FastAPI:
    app.include_router(api_router, prefix=settings.API_PREFIX)
    return app


def create_app() -> FastAPI:
    app = create_bare_app()
    app = attach_cors_middleware(app)
    app = attach_api_routes(app)
    return app


app = create_app()
