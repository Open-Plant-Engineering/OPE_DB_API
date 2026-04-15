from sqlalchemy import Column, String, Boolean, DateTime, BigInteger
from sqlalchemy.sql import func

from OPE_DB_API.db.base import Base


class SessionMetadata(Base):
    """
    Metadata table for edit sessions.

    Tracks ownership, lifecycle, and activity state.
    """

    __tablename__ = "sessions"

    session_id = Column(
        BigInteger,
        primary_key=True,
        nullable=False,
        doc="Externally generated (e.g. Snowflake) ID",
    )

    username = Column(
        String,
        nullable=True,
        index=True,
    )

    hostname = Column(
        String,
        nullable=True,
        index=True,
    )

    active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    ended_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )