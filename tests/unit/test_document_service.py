import sys
from pathlib import Path

# Add <project_root>/src to PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))

from ope_db_api.domain.services import DocumentService
from ope_db_api.domain.repositories import DocumentRepository
from ope_db_api.domain.exceptions import InvalidDocumentError
from ope_db_api.domain.models import Document


class InMemoryDocumentRepository(DocumentRepository):
    def __init__(self):
        self.documents = {}

    def save(self, document: Document) -> None:
        self.documents[document.id.value] = document

    def get_by_id(self, document_id):
        return self.documents.get(document_id.value)

    def list_all(self):
        return self.documents.values()


def test_create_document_success():
    repo = InMemoryDocumentRepository()
    service = DocumentService(repo)

    doc = service.create_document(
        name="Test Doc",
        payload={"a": 1}
    )

    assert doc.name == "Test Doc"
    assert doc.payload["a"] == 1


def test_create_document_without_name_raises_error():
    repo = InMemoryDocumentRepository()
    service = DocumentService(repo)

    try:
        service.create_document("", {})
        assert False, "Expected InvalidDocumentError"
    except InvalidDocumentError:
        assert True


def run_all_tests():
    test_create_document_success()
    test_create_document_without_name_raises_error()
    print("✅ All domain tests passed")


if __name__ == "__main__":
    run_all_tests()
