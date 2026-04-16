from sqlalchemy import Column, Integer, DateTime, BigInteger, Sequence
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from OPE_DB_API.db.base import Base


class DbDataHistoryBase(Base):
    """
    Base class for immutable history records.

    One row per CREATE / UPDATE / DELETE operation.
    """

    __abstract__ = True

    history_id = Column(
        BigInteger,
        primary_key=True,
        server_default=Sequence("history_id_seq").next_value(),
        doc="Externally generated (e.g. Snowflake) ID",
    )

    data_id = Column(
        BigInteger,
        nullable=False,
        index=True,
    )

    session_id = Column(
        BigInteger,
        nullable=False,
        index=True,
    )

    operation_type = Column(
        Integer,
        nullable=False,
    )

    old_value = Column(
        JSONB,
        nullable=True,
    )

    new_value = Column(
        JSONB,
        nullable=True,
    )