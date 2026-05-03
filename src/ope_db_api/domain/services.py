from typing import Dict, Any
from .models import Document, DocumentId
from .repositories import DocumentRepository
from .exceptions import InvalidDocumentError


class DocumentService:
    """
    Domain service responsible for document operations.
    """

    def __init__(self, repository: DocumentRepository):
        self._repository = repository

    def create_document(
        self,
        name: str,
        payload: Dict[str, Any]
    ) -> Document:
        if not name:
            raise InvalidDocumentError("Document name cannot be empty")

        document = Document(
            id=DocumentId.new(),
            name=name,
            payload=payload,
        )

        self._repository.save(document)
        return document