"""
Database Engine and Session Management

This module provides canonical creation of SQLAlchemy engines
and database sessions for the OPE Core platform.

This is pure infrastructure code.
"""

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def create_db_engine(
    database_url: str,
    *,
    echo: bool = False,
    future: bool = True,
) -> Engine:
    """
    Create and return a SQLAlchemy Engine.

    Args:
        database_url: SQLAlchemy-compatible database URL
        echo: Enable SQL echo for debugging
        future: Use SQLAlchemy 2.0 style engine

    Returns:
        SQLAlchemy Engine
    """
    return create_engine(
        database_url,
        echo=echo,
        future=future,
    )


def create_session_factory(engine: Engine) -> sessionmaker:
    """
    Create a SQLAlchemy session factory bound to the given engine.

    Args:
        engine: SQLAlchemy Engine

    Returns:
        A configured sessionmaker
    """
    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        future=True,
    )


@contextmanager
def db_session(session_factory: sessionmaker) -> Iterator[Session]:
    """
    Context manager for SQLAlchemy sessions.

    Ensures:
    - commit on success
    - rollback on failure
    - proper session close

    Usage:
        with db_session(SessionFactory) as session:
            ...
    """
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()