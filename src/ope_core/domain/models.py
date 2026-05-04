from dataclasses import dataclass
from typing import Any, Dict
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DocumentId:
    """
    Value object representing a document identifier.
    """

    value: UUID

    @staticmethod
    def new() -> "DocumentId":
        return DocumentId(uuid4())


@dataclass
class Document:
    """
    Aggregate root representing a JSONB document.
    """

    id: DocumentId
    name: str
    payload: Dict[str, Any]
