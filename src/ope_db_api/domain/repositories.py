from abc import ABC, abstractmethod
from typing import Iterable
from .models import Document, DocumentId


class DocumentRepository(ABC):
    """
    Abstract repository for documents.
    """

    @abstractmethod
    def save(self, document: Document) -> None:
        pass

    @abstractmethod
    def get_by_id(self, document_id: DocumentId) -> Document:
        pass

    @abstractmethod
    def list_all(self) -> Iterable[Document]:
        pass