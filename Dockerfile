ARG BASE_LAYER=base
FROM python:3.11.3-slim-buster as base
LABEL maintainer="Data Science & Engineering @ Wealthsimple <data@wealthsimple.com>"

##############################################

FROM $BASE_LAYER as backend-builder

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip install uv

WORKDIR /usr/src/app

# Copy requirements files first for caching
COPY --chown=nobody:nogroup requirements.txt requirements.dev.txt pyproject.toml ./

# Install dependencies
RUN uv pip install --system -r requirements.txt

# Copy remaining files, except those listed in .dockerignore
# This step is almost guaranteed to bust cache, so don't put anything heavy beyond this point.
COPY --chown=nobody:nogroup ./llm_gateway/ ./llm_gateway/
COPY --chown=nobody:nogroup ./README.md ./README.md
COPY --chown=nobody:nogroup ./alembic.ini ./alembic.ini
COPY --chown=nobody:nogroup ./alembic/ ./alembic/

##############################################

FROM backend-builder as backend-test-suite

RUN uv pip install --system -r requirements.dev.txt

# Install the package in editable mode
RUN uv pip install --system -e .

COPY --chown=nobody:nogroup ./tests/ ./tests/

CMD ["pytest"]

##############################################

FROM node:16.13.1 as frontend-pre-builder

WORKDIR /usr/src/app

# Install dependencies
COPY front_end/package.json front_end/yarn.lock front_end/.eslintrc.json front_end/tsconfig.json front_end/.env-cmdrc ./
RUN yarn install

##############################################

FROM frontend-pre-builder as frontend-builder-staging

# Build ready for Staging
COPY ./front_end ./
RUN yarn build-staging

##############################################

FROM frontend-pre-builder as frontend-builder-production

# Build ready for Production
COPY ./front_end ./
RUN yarn build-production

##############################################

# Copy frontend build artifacts into the backend image
FROM backend-builder as application

# Install production dependencies only
RUN uv pip install --system -r requirements.txt

COPY --from=frontend-builder-production /usr/src/app/build/ /usr/src/app/front_end/build-production/
COPY --from=frontend-builder-staging /usr/src/app/build/ /usr/src/app/front_end/build-staging/
