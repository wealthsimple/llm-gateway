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

import logging
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker

from llm_gateway.constants import get_settings

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

settings = get_settings()


class DB:
    """
    Class for managing connections to the logging DB
    """

    def __init__(self) -> None:
        self.db_url = settings.DATABASE_URL

    def create_db_engine(self) -> Engine:
        """
        Create DB engine from url

        :return: Database engine created
        :rtype: Engine
        """
        return create_engine(self.db_url.replace("postgresql+asyncpg", "postgresql"))


@contextmanager
def get_session() -> Iterator[Session]:
    """
    Open a DB session

    :raises Exception: Raised if session fails for some reason
    :yield: DB session
    :rtype: Iterator[Session]
    """
    llm_gateway_db = DB()
    session_factory = sessionmaker(
        bind=llm_gateway_db.create_db_engine(), expire_on_commit=False
    )
    session = session_factory()
    try:
        logging.debug("Opening new database session")
        yield session
        logging.debug("Committing database session")
        session.commit()
        logging.debug("Session committed successfully")
    except Exception as e:
        logging.error(f"Database error: {str(e)}")
        logging.debug("Rolling back database session")
        session.rollback()
        raise Exception(f"Rolling back due to {e}")
    finally:
        logging.debug("Closing database session")
        session.close()
