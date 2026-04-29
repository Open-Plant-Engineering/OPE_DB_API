"""
Top-level compatibility package for FreeCAD.

This file makes the inner OPE_DB_API package importable as if it were
installed via pip.
"""

import os
import sys

# Absolute path to the inner package
_inner_pkg_path = os.path.join(os.path.dirname(__file__), "OPE_DB_API")

__path__ = [_inner_pkg_path]

# Ensure Python can find submodules like OPE_DB_API.cache, OPE_DB_API.db, etc.
if _inner_pkg_path not in sys.path:
    sys.path.insert(0, _inner_pkg_path)

# Re-export inner package symbols safely
from OPE_DB_API import *  # noqa: F401,F403