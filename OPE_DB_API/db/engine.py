from typing import Dict, Tuple
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from OPE_DB_API.config import get_config, get_client_config


# ---------------------------------------------------------
# Engine cache: one engine per project/code
# ---------------------------------------------------------

_SERVER_ENGINES: Dict[str, Engine] = {}
_CLIENT_ENGINES: Dict[str, Engine] = {}


def get_engine(code: str, echo:bool = False) -> Engine:
    """
    Return a SQLAlchemy engine for the given project code.

    Engines are created lazily and cached per code.
    """
    if code in _SERVER_ENGINES:
        return _SERVER_ENGINES[code]

    config = get_config()
    try:
        pg_cfg = config[config["database_map"][code.upper()]]
        db_url = (
            f"postgresql+psycopg2://{pg_cfg['user']}:{pg_cfg['password']}"
            f"@{pg_cfg['host']}:{pg_cfg['port']}/{pg_cfg['database']}"
        )
        
    except KeyError:
        raise KeyError(
            f"No database configuration found for project '{code}'"
        )

    engine = create_engine(
        db_url,
        future=True,
        pool_pre_ping=True,
        echo=echo,
    )

    _SERVER_ENGINES[code] = engine
    return engine


# ---------------------------------------------------------
# Client-side (local cache) engine
# ---------------------------------------------------------

def get_client_engine(code: str, echo:bool = False) -> Engine:
    """
    Return a SQLAlchemy engine for the client-side local cache DB.

    Engines are created lazily and cached per project code.
    """
    if code in _CLIENT_ENGINES:
        return _CLIENT_ENGINES[code]

    config = get_client_config()
    try:
        pg_cfg = config[config["database_map"][code.upper()]]
        db_url = (
            f"postgresql+psycopg2://{pg_cfg['user']}:{pg_cfg['password']}"
            f"@{pg_cfg['host']}:{pg_cfg['port']}/{pg_cfg['database']}"
        )
        
    except KeyError:
        raise KeyError(
            f"No database configuration found for project '{code}'"
        )

    engine = create_engine(
        db_url,
        future=True,
        pool_pre_ping=True,
        echo=echo,
    )

    _CLIENT_ENGINES[code] = engine
    return engine