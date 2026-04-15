from sqlalchemy import Column, Integer, Index, BigInteger
from sqlalchemy.dialects.postgresql import JSONB

from OPE_DB_API.db.base import Base


class DbDataOverlayBase(Base):
    """
    Base class for session-scoped overlay (draft) data.

    Represents proposed changes during a session.

    ID is generated externally (client/tool).
    """

    __abstract__ = True

    overlay_id = Column(
        BigInteger,
        primary_key=True,
        nullable=False,
        index=True,
        doc="Externally generated (e.g. Snowflake) ID",
    )

    session_id = Column(
        BigInteger,
        nullable=False,
        index=True,
    )

    node_id = Column(
        BigInteger,
        nullable=False,
    )

    attribute_id = Column(
        Integer,
        nullable=False,
    )

    value = Column(
        JSONB,
        nullable=True,
    )