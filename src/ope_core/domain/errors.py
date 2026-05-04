"""
Domain Errors

This module defines domain-level exceptions used across
the OPE Core platform.

Domain errors represent semantic violations, not
technical failures.
"""


class DomainError(Exception):
    """Base class for all domain-level errors."""


class InactiveSessionError(DomainError):
    """Raised when an operation is attempted on an inactive session."""


class SnapshotRequiredError(DomainError):
    """Raised when history is applied before a snapshot."""


class InvalidHistoryError(DomainError):
    """Raised when a history batch is invalid or unsupported."""