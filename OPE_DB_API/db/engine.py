from typing import Dict, Tuple
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from OPE_DB_API.config import get_config


# ---------------------------------------------------------
# Engine cache: one engine per project/code
# ---------------------------------------------------------

_ENGINES: Dict[str, Engine] = {}


def get_engine(code: str) -> Engine:
    """
    Return a SQLAlchemy engine for the given project code.

    Engines are created lazily and cached per code.
    """
    if code in _ENGINES:
        return _ENGINES[code]

    config = get_config()
    try:
        db_url = config["projects"][code]["database_url"]
    except KeyError:
        raise KeyError(
            f"No database configuration found for project '{code}'"
        )

    engine = create_engine(
        db_url,
        future=True,
        pool_pre_ping=True,
    )

    _ENGINES[code] = engine
    return engine