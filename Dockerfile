ARG BASE_LAYER=base
FROM python:3.11.3-slim-buster as base
LABEL maintainer="Data Science & Engineering @ Wealthsimple <data@wealthsimple.com>"

##############################################

# This layer is only intended for local dev.
# It manually compiles librdkafka so that everything else works on M1.
# it also uses a public, infrequently-changing Docker image
# so that this step can be run less often.
# It should get skipped during a normal build

FROM python:3.11-bullseye as base-dev

##############################################

FROM $BASE_LAYER as backend-builder

WORKDIR /usr/src/app
RUN pip install poetry==1.3.2

# Copy pyproject and lock files first. This allows us to cache
# dependencies even when source files are changed.
COPY --chown=nobody:nogroup poetry.lock pyproject.toml ./

# Install dependencies.
ENV PATH="${PATH}:/root/.local/share/pypoetry/venv/bin"
RUN poetry config virtualenvs.create false
RUN poetry config installer.max-workers 2
RUN poetry install --no-interaction --no-root

# Copy remaining files, except those listed in .dockerignore
# This step is almost guaranteed to bust cache, so don't put anything heavy beyond this point.
COPY --chown=nobody:nogroup ./llm_gateway/ ./llm_gateway/
COPY --chown=nobody:nogroup ./README.md ./README.md
COPY --chown=nobody:nogroup ./alembic.ini ./alembic.ini
COPY --chown=nobody:nogroup ./alembic/ ./alembic/

##############################################

FROM node:16.13.1 as frontend-builder
WORKDIR /usr/src/app

# Install dependencies
COPY front_end/package.json front_end/yarn.lock front_end/.eslintrc.json front_end/tsconfig.json ./
RUN yarn install

COPY ./front_end ./
RUN yarn build

##############################################

FROM nginx:1.19.2-alpine as application

COPY --from=frontend-builder /usr/src/app/build/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

