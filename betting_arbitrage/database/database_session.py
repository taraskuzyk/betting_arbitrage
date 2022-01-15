import sqlalchemy
from sqlalchemy import and_
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql.dml import UpdateBase

from database.orm.base import Base


class DatabaseSession:
    def __init__(self, session: Session):
        self._session = session

    def query(self, *args) -> Query:
        return self._session.query(*args)

    def commit(self):
        self._session.commit()

    def bulk_update_mappings(self, *args, **kwargs):
        self._session.bulk_update_mappings(*args, **kwargs)

    def bulk_insert_mappings(self, *args, **kwargs):
        self._session.bulk_insert_mappings(*args, **kwargs)

    def rollback(self):
        self._session.rollback()

    def add_all(self, entries, commit=False):
        self._session.add_all(entries)
        if commit:
            self.commit()

    def add(self, entry, commit=False):
        self._session.add(entry)
        if commit:
            self.commit()

    def delete(self, entry, commit=False):
        self._session.delete(entry)
        if commit:
            self.commit()

    def close_session(self):
        self._session.close()

    def query_like(self, orm_object: Base) -> Query:
        orm_dict = orm_object.__dict__
        orm_class = type(orm_object)
        conditions = [
            orm_class.__dict__[key] == orm_dict[key]
            for key in orm_dict.keys()
            if not _is_key_private(key)
        ]
        all_conditions_are_met = and_(*conditions)
        return self.query(orm_class).where(all_conditions_are_met)

    def execute(self, statement: UpdateBase or sqlalchemy.text):
        self._session.autoflush = False
        self._session.execute(statement, execution_options=dict(autocommit=False))


def _is_key_private(key: str) -> bool:
    return key[0] == "_"
