import os
import tomllib
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------
# Default config file location (unchanged behavior)
# ---------------------------------------------------------

_DEFAULT_CONFIG_FILE = Path(
    os.path.dirname(__file__)
).parent / "defaults" / "config.toml"

# ---------------------------------------------------------
# Runtime override (NEW)
# ---------------------------------------------------------

_config_file_path: Optional[Path] = None

_cached_config = None
_cached_mtime = 0.0


# ---------------------------------------------------------
# Public API: explicitly set config file path (NEW)
# ---------------------------------------------------------

def set_config_file(path: str | os.PathLike) -> None:
    """
    Override the configuration file path at runtime.

    Must be called before get_config() is used.
    Automatically clears cached config.
    """
    global _config_file_path, _cached_config, _cached_mtime

    _config_file_path = Path(path).resolve()
    _cached_config = None
    _cached_mtime = 0.0


# ---------------------------------------------------------
# Internal: resolve config file path (NEW)
# ---------------------------------------------------------

def _resolve_config_file() -> Path:
    """
    Resolve config file using precedence:
    1. set_config_file()
    2. OPE_DB_API_CONFIG env variable
    3. Package default
    """
    if _config_file_path is not None:
        return _config_file_path

    env_path = os.getenv("OPE_DB_API_CONFIG")
    if env_path:
        return Path(env_path).resolve()

    return _DEFAULT_CONFIG_FILE


# ---------------------------------------------------------
# Load and cache config (existing logic, slightly adapted)
# ---------------------------------------------------------

def get_config(force_reload: bool = False) -> dict:
    """
    Load and cache config.toml.

    - Reloads automatically if file is modified
    - Supports runtime override and env-based config
    - Returns config as a dictionary
    """
    global _cached_config, _cached_mtime

    config_file = _resolve_config_file()

    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    mtime = config_file.stat().st_mtime

    if force_reload or _cached_config is None or mtime != _cached_mtime:
        with config_file.open("rb") as f:
            _cached_config = tomllib.load(f)
        _cached_mtime = mtime

    return _cached_config
