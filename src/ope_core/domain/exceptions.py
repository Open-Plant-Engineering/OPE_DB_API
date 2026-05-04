class DomainError(Exception):
    """Base class for domain-level exceptions."""

    pass


class DocumentNotFoundError(DomainError):
    pass


class InvalidDocumentError(DomainError):
    pass
