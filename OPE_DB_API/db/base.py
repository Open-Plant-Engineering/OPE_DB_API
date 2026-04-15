from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    All live data, overlay data, and history data models
    must inherit from this base.
    """
    pass