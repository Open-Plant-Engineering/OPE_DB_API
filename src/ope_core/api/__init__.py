"""
API Layer Package

The API layer exposes OPE Core functionality over HTTP.

Responsibilities:
- HTTP request/response handling
- Input validation
- Output serialization

Rules:
- API code may depend on ope_core.domain
- API code may depend on ope_core.replica
- API code must NOT contain business logic
- API code must NOT access the database directly
"""

__all__ = []