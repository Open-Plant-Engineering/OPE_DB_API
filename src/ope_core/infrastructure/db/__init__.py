"""
Database Infrastructure Package

This package contains database-related infrastructure components
for the OPE Core platform.

Responsibilities:
- Database engine creation
- Connection/session management
- Concrete persistence adapters

Rules:
- Infrastructure code may depend on external libraries (SQLAlchemy, psycopg)
- Infrastructure code may depend on ope_core.domain
- Infrastructure code may implement replica adapter protocols
- Infrastructure code must NOT define domain meaning
"""

__all__ = []