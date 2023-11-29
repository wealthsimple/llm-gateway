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

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta

from llm_gateway.constants import get_settings

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
        return create_engine(self.db_url)


@contextmanager
def db_session_scope() -> Iterator[None]:
    """
    Open a connected DB session

    :raises Exception: Raised if session fails for some reason
    :yield: DB session
    :rtype: Iterator[None]
    """
    llm_gateway_db = DB()
    session = sessionmaker(bind=llm_gateway_db.create_db_engine())
    session = session()
    try:
        yield session
        session.commit()
    except Exception as e:  # noqa
        session.rollback()
        raise Exception(f"Rolling back due to {e}")
    finally:
        session.close()


def write_record_to_db(db_record: DeclarativeMeta) -> None:
    """
    Used in routes to log data as a background task to the database

    :param db_record: Populated DB Model defined in db.models, initialized with data
    :type db_record: DeclarativeMeta
    """
    with db_session_scope() as session:
        session.add(db_record)
