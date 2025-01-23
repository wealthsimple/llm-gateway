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

RUN pip install poetry==1.3.2

WORKDIR /usr/src/app

RUN poetry config virtualenvs.in-project true
RUN poetry config virtualenvs.create false --local

# Copy pyproject and lock files first. This allows us to cache
# dependencies even when source files are changed.
COPY --chown=nobody:nogroup poetry.lock pyproject.toml ./

# Install dependencies.
RUN poetry install --only main --no-interaction --no-root

# Copy remaining files, except those listed in .dockerignore
# This step is almost guaranteed to bust cache, so don't put anything heavy beyond this point.
COPY --chown=nobody:nogroup ./llm_gateway/ ./llm_gateway/
COPY --chown=nobody:nogroup ./README.md ./README.md
COPY --chown=nobody:nogroup ./alembic.ini ./alembic.ini
COPY --chown=nobody:nogroup ./alembic/ ./alembic/

##############################################

FROM backend-builder as backend-test-suite

RUN poetry install --no-interaction --no-root

# when running poetry without venvs, it fails to install the llm_gateway package
RUN pip install -e .

COPY --chown=nobody:nogroup ./tests/ ./tests/

CMD ["pytest"]

##############################################

FROM node:22.13.1 as frontend-pre-builder

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
COPY --from=frontend-builder-production /usr/src/app/build/ /usr/src/app/front_end/build-production/
COPY --from=frontend-builder-staging /usr/src/app/build/ /usr/src/app/front_end/build-staging/
