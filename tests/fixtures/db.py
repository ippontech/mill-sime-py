from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import Engine, StaticPool, create_engine, text
from sqlmodel import SQLModel


@contextmanager
def get_sqlite_engine() -> Iterator[Engine]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    with engine.connect() as connection:
        SQLModel.metadata.create_all(bind=engine)
        connection.execute(text("PRAGMA foreign_keys=ON"))
        connection.commit()

    yield engine

    engine.dispose()
