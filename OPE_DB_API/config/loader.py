import os
import tomllib
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------
# Package-default configuration file
# ---------------------------------------------------------

_DEFAULT_CONFIG_FILE = (
    Path(__file__).resolve()
    .parent.parent
    / "defaults"
    / "config.toml"
)


# ---------------------------------------------------------
# Runtime override state (explicit, controlled)
# ---------------------------------------------------------

_config_file_path: Optional[Path] = None


# ---------------------------------------------------------
# Cached configuration
# ---------------------------------------------------------

_cached_config: Optional[dict] = None
_cached_mtime: float = 0.0


# ---------------------------------------------------------
# Public API: override config file path
# ---------------------------------------------------------

def set_config_file(path: str | os.PathLike) -> None:
    """
    Explicitly override the configuration file path.

    This function should be called during application startup
    (before the config is first accessed).

    Calling this function will automatically reset the
    cached configuration.
    """
    global _config_file_path, _cached_config, _cached_mtime

    _config_file_path = Path(path).expanduser().resolve()
    _cached_config = None
    _cached_mtime = 0.0


# ---------------------------------------------------------
# Internal: resolve config file location
# ---------------------------------------------------------

def _resolve_config_file() -> Path:
    """
    Resolve configuration file path with the following precedence:

    1. Runtime override via set_config_file()
    2. Environment variable OPE_DB_API_CONFIG
    3. Package default config file
    """
    if _config_file_path is not None:
        return _config_file_path

    env_path = os.getenv("OPE_DB_API_CONFIG")
    if env_path:
        return Path(env_path).expanduser().resolve()

    return _DEFAULT_CONFIG_FILE


# ---------------------------------------------------------
# Public API: load configuration
# ---------------------------------------------------------

def get_config(force_reload: bool = False) -> dict:
    """
    Load and return the application configuration.

    The configuration is cached and reloaded only if:
    - force_reload is True
    - the config file has changed on disk

    Returns:
        dict: Parsed configuration data
    """
    global _cached_config, _cached_mtime

    config_file = _resolve_config_file()

    if not config_file.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_file}"
        )

    mtime = config_file.stat().st_mtime

    if (
        force_reload
        or _cached_config is None
        or mtime != _cached_mtime
    ):
        with config_file.open("rb") as f:
            _cached_config = tomllib.load(f)

        _cached_mtime = mtime

    return _cached_config