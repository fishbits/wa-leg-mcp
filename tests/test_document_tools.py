"""
Unit tests for document management tools.
"""

import pytest
from unittest.mock import patch

from src.wa_leg_mcp.tools.document_tools import (
    get_all_documents_by_class,
    get_document_classes,
    get_documents_by_class,
)


@pytest.fixture
def mock_wsl_client():
    """Mock WSLClient for testing."""
    with patch("src.wa_leg_mcp.tools.document_tools.WSLClient") as mock_class:
        yield mock_class.return_value


class TestGetDocumentClasses:
    """Tests for get_document_classes function."""

    def test_success(self, mock_wsl_client):
        """Test successful retrieval of document classes."""
        mock_classes = [
            {"name": "Bills", "description": "Legislative bills"},
            {"name": "Amendments", "description": "Bill amendments"},
        ]
        mock_wsl_client.get_document_classes.return_value = mock_classes

        result = get_document_classes("2023-24")

        assert result["success"] is True
        assert len(result["data"]) == 2
        assert result["metadata"]["count"] == 2
        assert result["metadata"]["biennium"] == "2023-24"

    def test_empty(self, mock_wsl_client):
        """Test retrieval when no document classes found."""
        mock_wsl_client.get_document_classes.return_value = []

        result = get_document_classes("2023-24")

        assert result["success"] is True
        assert result["data"] == []
        assert "No document classes found" in result["metadata"]["message"]

    def test_api_failure(self, mock_wsl_client):
        """Test handling of API failure."""
        mock_wsl_client.get_document_classes.return_value = None

        result = get_document_classes("2023-24")

        assert result["success"] is False
        assert "Failed to retrieve document classes" in result["error"]

    def test_exception_handling(self, mock_wsl_client):
        """Test handling of unexpected exceptions."""
        mock_wsl_client.get_document_classes.side_effect = Exception("Network error")

        result = get_document_classes("2023-24")

        assert result["success"] is False
        assert "An error occurred" in result["error"]


class TestGetAllDocumentsByClass:
    """Tests for get_all_documents_by_class function."""

    def test_success(self, mock_wsl_client):
        """Test successful retrieval of documents by class."""
        mock_documents = [
            {
                "name": "HB 1000",
                "class": "Bills",
                "url": "http://example.com/hb1000.pdf",
                "bill_id": "HB 1000",
            },
            {
                "name": "HB 1001",
                "class": "Bills",
                "url": "http://example.com/hb1001.pdf",
                "bill_id": "HB 1001",
            },
        ]
        mock_wsl_client.get_all_documents_by_class.return_value = mock_documents

        result = get_all_documents_by_class("2023-24", "Bills")

        assert result["success"] is True
        assert len(result["data"]) == 2
        assert result["metadata"]["count"] == 2
        assert result["metadata"]["document_class"] == "Bills"

    def test_empty(self, mock_wsl_client):
        """Test retrieval when no documents found."""
        mock_wsl_client.get_all_documents_by_class.return_value = []

        result = get_all_documents_by_class("2023-24", "Amendments")

        assert result["success"] is True
        assert result["data"] == []
        assert "No documents found" in result["metadata"]["message"]
        assert "Amendments" in result["metadata"]["message"]

    def test_api_failure(self, mock_wsl_client):
        """Test handling of API failure."""
        mock_wsl_client.get_all_documents_by_class.return_value = None

        result = get_all_documents_by_class("2023-24", "Bills")

        assert result["success"] is False
        assert "Failed to retrieve documents" in result["error"]

    def test_large_result_set(self, mock_wsl_client):
        """Test handling of large result sets."""
        mock_documents = [
            {
                "name": f"HB {1000 + i}",
                "class": "Bills",
                "url": f"http://example.com/hb{1000 + i}.pdf",
                "bill_id": f"HB {1000 + i}",
            }
            for i in range(150)
        ]
        mock_wsl_client.get_all_documents_by_class.return_value = mock_documents

        result = get_all_documents_by_class("2023-24", "Bills")

        assert result["success"] is True
        assert len(result["data"]) == 150
        assert result["metadata"]["count"] == 150


class TestGetDocumentsByClass:
    """Tests for get_documents_by_class function."""

    def test_success(self, mock_wsl_client):
        """Test successful retrieval of documents with filter."""
        mock_documents = [
            {
                "name": "HB 1000",
                "class": "Bills",
                "url": "http://example.com/hb1000.pdf",
                "bill_id": "HB 1000",
            },
            {
                "name": "HB 1001",
                "class": "Bills",
                "url": "http://example.com/hb1001.pdf",
                "bill_id": "HB 1001",
            },
        ]
        mock_wsl_client.get_documents_by_class.return_value = mock_documents

        result = get_documents_by_class("2023-24", "Bills", "HB 1*")

        assert result["success"] is True
        assert len(result["data"]) == 2
        assert result["metadata"]["count"] == 2
        assert result["metadata"]["name_filter"] == "HB 1*"

    def test_empty(self, mock_wsl_client):
        """Test retrieval when no matching documents found."""
        mock_wsl_client.get_documents_by_class.return_value = []

        result = get_documents_by_class("2023-24", "Bills", "HB 9999")

        assert result["success"] is True
        assert result["data"] == []
        assert "No documents found" in result["metadata"]["message"]
        assert "HB 9999" in result["metadata"]["message"]

    def test_wildcard_filter(self, mock_wsl_client):
        """Test with wildcard filter pattern."""
        mock_documents = [
            {
                "name": "SB 5000",
                "class": "Bills",
                "url": "http://example.com/sb5000.pdf",
                "bill_id": "SB 5000",
            }
        ]
        mock_wsl_client.get_documents_by_class.return_value = mock_documents

        result = get_documents_by_class("2023-24", "Bills", "SB 5*")

        assert result["success"] is True
        assert len(result["data"]) == 1
        mock_wsl_client.get_documents_by_class.assert_called_once_with("2023-24", "Bills", "SB 5*")

    def test_api_failure(self, mock_wsl_client):
        """Test handling of API failure."""
        mock_wsl_client.get_documents_by_class.return_value = None

        result = get_documents_by_class("2023-24", "Bills", "HB 1*")

        assert result["success"] is False
        assert "Failed to retrieve documents" in result["error"]

    def test_exception_handling(self, mock_wsl_client):
        """Test handling of unexpected exceptions."""
        mock_wsl_client.get_documents_by_class.side_effect = Exception("Network error")

        result = get_documents_by_class("2023-24", "Bills", "HB 1*")

        assert result["success"] is False
        assert "An error occurred" in result["error"]

    def test_metadata_includes_all_parameters(self, mock_wsl_client):
        """Test that metadata includes all input parameters."""
        mock_wsl_client.get_documents_by_class.return_value = []

        result = get_documents_by_class("2023-24", "Amendments", "HB 1234")

        assert result["metadata"]["biennium"] == "2023-24"
        assert result["metadata"]["document_class"] == "Amendments"
        assert result["metadata"]["name_filter"] == "HB 1234"
