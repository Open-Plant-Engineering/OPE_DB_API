"""
Configuration subsystem for ope_db_api.

Provides safe, explicit, and overridable access
to application configuration.
"""

from .loader import get_config, set_config_file

__all__ = [
    "get_config",
    "set_config_file",
]