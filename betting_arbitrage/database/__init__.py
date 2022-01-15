from pathlib import Path

from sqlalchemy import (
    create_engine,
    MetaData,
    exists,
    select,
    text,
)
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from sqlalchemy.sql.ddl import DropSchema, CreateSchema

from database.database_session import DatabaseSession
from database.orm.bet import Bet

def get_sqlite_url_from_path(path: Path):
    return f"sqlite:///{path}"


class Database(DatabaseSession):
    def __init__(
        self,
        url: str,
        metadata: MetaData,
        should_create_schema=False,
        echo=False,
        pool_pre_ping=False,
        autoflush=True
    ):
        self._url = url
        self._echo = echo
        self._metadata = metadata
        self._metadata.schema = "test"
        self._pool_pre_ping = pool_pre_ping
        self.autoflush = autoflush

        if should_create_schema:
            if "amazon" in url:
                raise ValueError(
                    "You're formatting an AWS link. Can't let you do that."
                )
            if "sqlite" not in url:
                self._create_schema_from_url(url)
            else:
                self.drop_schemas(url)

        self.engine = self._get_engine(url)

        if should_create_schema:
            self._create_all_tables()

        super().__init__(self.get_session())

    def _get_engine(self, url):
        return create_engine(url, echo=self._echo, pool_pre_ping=self._pool_pre_ping)

    def _create_schema_from_url(self, url):
        schema_name = self._get_schema_name_from_url(url)
        url_with_no_schema = url[: -len(schema_name)]

        if not self._does_schema_exist(url, schema_name):
            self.engine = self._get_engine(url)
            self._create_schema(schema_name)
        else:
            self.engine = self._get_engine(url)
            self._recreate_schema(schema_name)

    def _does_schema_exist(self, url, schema_name):
        engine = self._get_engine(url)
        session = Session(engine)
        query = exists(
            select(text("schema_name"))
            .select_from(text("information_schema.schemata"))
            .where(text(f"schema_name = '{schema_name}'"))
        )
        return session.query(query).scalar()

    def drop_schemas(self, url):
        # different approach because sqlite has no schemas
        self.engine = self._get_engine(url)
        try:
            self._drop_all_tables()
        except OperationalError:
            pass

    @staticmethod
    def _get_schema_name_from_url(url):
        return url.split("/")[-1]

    @classmethod
    def from_sqlite_db_path(
        cls, path: Path, metadata: MetaData, should_create_schema=False, echo=False
    ):
        url = get_sqlite_url_from_path(path)
        return cls(url, metadata, should_create_schema=should_create_schema, echo=echo)

    def _create_schema(self, name):
        self.engine.execute(CreateSchema(name))

    def _drop_schema(self, name):
        self.engine.execute(DropSchema(name, cascade=True))
        self.engine.execute(
            text("DROP TYPE IF EXISTS contactsource; DROP TYPE IF EXISTS emailsource")
        )

    def _drop_all_tables(self):
        for table in reversed(self._metadata.sorted_tables):
            table.drop(self.engine)

    def _recreate_schema(self, name):
        self._drop_schema(name)
        self._create_schema(name)

    def _create_all_tables(self):
        for table in self._metadata.sorted_tables:
            table.create(self.engine, checkfirst=True)

    def get_session(self):
        return Session(self.engine, autoflush=self.autoflush)

    def refresh_session(self):
        self._session = Session(self.engine, autoflush=self.autoflush)

    def clear(self):
        """completely erases DB contents"""
        for table in reversed(self._metadata.sorted_tables):
            self._session.execute(table.delete())
        self.commit()


class DatabaseMixin:
    def __init__(self, db: Database):
        self._db = db


from database.orm.bet import Bet