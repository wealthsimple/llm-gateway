ARG BASE_LAYER=base
FROM python:3.11.3-slim-buster1 as base
LABEL maintainer="Data Science & Engineering @ Wealthsimple <data@wealthsimple.com>"

##############################################

# This layer is only intended for local dev.
# It manually compiles librdkafka so that everything else works on M1.
# it also uses a public, infrequently-changing Docker image
# so that this step can be run less often.
# It should get skipped during a normal build

FROM python:3.11-bullseye as base-dev

##############################################

FROM $BASE_LAYER as builder

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

FROM builder as test-suite

RUN poetry install --no-interaction --no-root

# when running poetry without venvs, it fails to install the llm_gateway package
RUN pip install -e .

COPY --chown=nobody:nogroup ./tests/ ./tests/

CMD ["pytest"]

##############################################

FROM builder as application

# fastapi server port
EXPOSE 5000 5000

CMD ["uvicorn", "--host", "0.0.0.0","--port", "5000", "llm_gateway.app:app"]
