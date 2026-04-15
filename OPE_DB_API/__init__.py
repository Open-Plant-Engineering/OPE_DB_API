"""
ope_db_api

A session-based database data management engine.

Designed to be used as a plug-and-play FastAPI backend component
with draft → overlay → commit workflows.
"""

from .app import create_app

__all__ = [
    "create_app",
]

__version__ = "0.1.0"