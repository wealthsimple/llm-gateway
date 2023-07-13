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

import pathlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from llm_gateway.routers import cohere_api, openai_api


def create_bare_app() -> FastAPI:
    app = FastAPI()
    app.title = "LLM Proxy"
    app.description = "LLM Proxy Developed by Wealthsimple"
    return app


def attach_api_service(app: FastAPI) -> FastAPI:
    api = FastAPI(openapi_prefix="/api")
    api.include_router(openai_api.router, prefix="/openai")
    api.include_router(cohere_api.router, prefix="/cohere")

    @api.get("/healthcheck")
    async def healthcheck():
        """
        Endpoint to verify that the service is up and running
        """
        return {"message": "llm-gateway is healthy"}

    app.mount("/api", api, name="api")
    return app


def attach_middleware(app: FastAPI) -> FastAPI:
    # Allow Front-end Origin in local development
    origins = ["http://localhost:3000", "http://localhost:5000"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def mount_front_end(app: FastAPI) -> FastAPI:
    FRONT_END_BUILD_DIRECTORY = (
        pathlib.Path(__file__).parent.parent / "front_end" / "build"
    )
    app.mount(
        "/assets",
        StaticFiles(directory=FRONT_END_BUILD_DIRECTORY / "assets"),
        name="assets",
    )

    app.mount(
        "/static",
        StaticFiles(directory=FRONT_END_BUILD_DIRECTORY / "static"),
        name="static",
    )

    app.mount(
        "/styles",
        StaticFiles(directory=FRONT_END_BUILD_DIRECTORY / "styles"),
        name="styles",
    )

    @app.get("/")
    async def home() -> HTMLResponse:
        with open(FRONT_END_BUILD_DIRECTORY / "index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())

    return app


def create_app() -> FastAPI:
    app = create_bare_app()
    app = attach_middleware(app)
    app = mount_front_end(app)
    app = attach_api_service(app)
    return app


app = create_app()
