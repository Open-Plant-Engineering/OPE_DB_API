import pytest
from ope_core.core.errors import (
    OpeCoreError,
    SessionError,
    SessionNotActiveError,
    SessionNotFoundError,
)

def test_session_not_active_error_message():
    """
    Ensures the error message includes the session id exactly as expected.
    """
    exc = SessionNotActiveError(42)
    assert str(exc) == "Session 42 is not active"

def test_session_not_active_error_inheritance():
    """
    Ensures SessionNotActiveError is a proper domain error.
    """
    exc = SessionNotActiveError(1)
    assert isinstance(exc, SessionError)
    assert isinstance(exc, OpeCoreError)
    assert isinstance(exc, Exception)

def test_session_not_found_error_message():
    """
    Ensures SessionNotFoundError formats its message correctly.
    """
    exc = SessionNotFoundError(99)
    assert str(exc) == "Session 99 not found"
