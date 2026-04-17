from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.dialects.postgresql import JSONB

from OPE_DB_API.db.base import Base


class DbDataBase(Base):
    """
    Base class for live, authoritative data.

    Represents the committed state of an attribute/entity.
    """

    __abstract__ = True

    data_id = Column(
        BigInteger,
        primary_key=True,
        nullable=False,
        doc="Externally generated (e.g. Snowflake) ID",
    )

    node_id = Column(
        BigInteger,
        nullable=False,
        index=True,
    )

    attribute_id = Column(
        Integer,
        nullable=False,
        index=True,
    )

    value = Column(
        JSONB,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("node_id", "attribute_id", name="uq_node_attribute"),
    )
