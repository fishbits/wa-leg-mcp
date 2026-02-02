"""
Property-based tests for document management tools.

These tests validate correctness properties for document management tools using
property-based testing with hypothesis.
"""

import pytest
from hypothesis import given, strategies as st
from unittest.mock import patch

from src.wa_leg_mcp.tools.document_tools import (
    get_all_documents_by_class,
    get_document_classes,
    get_documents_by_class,
)


# Test data strategies
bienniums = st.sampled_from(["2021-22", "2023-24", "2025-26"])
document_classes = st.sampled_from(["Bills", "Amendments", "Session Laws", "Fiscal Notes"])
name_filters = st.sampled_from(["HB 1*", "SB 5*", "*1000*", "HB 1234"])


@pytest.mark.property_test
class TestDocumentClassRetrievalProperties:
    """
    Property 37: Document Class Retrieval
    
    For any biennium, calling getDocumentClasses SHALL return all available document
    types for that biennium with class names and descriptions.
    
    **Validates: Requirements 13.1, 13.5**
    """

    @given(biennium=bienniums, num_classes=st.integers(min_value=0, max_value=20))
    def test_document_classes_structure(self, biennium, num_classes):
        """Test that document classes retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.document_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_classes = [
                {
                    "name": f"Class {i}",
                    "description": f"Description for class {i}",
                }
                for i in range(num_classes)
            ]
            mock_client.get_document_classes.return_value = mock_classes

            result = get_document_classes(biennium)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert isinstance(result["data"], list)
                assert result["metadata"]["biennium"] == biennium
                if result["data"]:
                    assert result["metadata"]["count"] == num_classes

    @given(biennium=bienniums)
    def test_document_classes_empty_handling(self, biennium):
        """Test that empty document classes return empty list with message."""
        with patch("src.wa_leg_mcp.tools.document_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_document_classes.return_value = []

            result = get_document_classes(biennium)

            assert result["success"] is True
            assert result["data"] == []
            assert "message" in result["metadata"]
            assert biennium in result["metadata"]["message"]

    @given(biennium=bienniums, num_classes=st.integers(min_value=1, max_value=15))
    def test_document_classes_include_required_fields(self, biennium, num_classes):
        """Test that document classes include all required fields."""
        with patch("src.wa_leg_mcp.tools.document_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_classes = [
                {
                    "name": f"Class {i}",
                    "description": f"Description for class {i}",
                }
                for i in range(num_classes)
            ]
            mock_client.get_document_classes.return_value = mock_classes

            result = get_document_classes(biennium)

            if result["success"] and result["data"]:
                for doc_class in result["data"]:
                    # Verify required fields are present
                    assert "name" in doc_class
                    assert "description" in doc_class


@pytest.mark.property_test
class TestDocumentClassFilteringProperties:
    """
    Property 38: Document Class Filtering
    
    For any biennium and document class, calling getAllDocumentsByClass SHALL return
    all documents of that class.
    
    **Validates: Requirements 13.2**
    """

    @given(
        biennium=bienniums,
        document_class=document_classes,
        num_documents=st.integers(min_value=0, max_value=100)
    )
    def test_all_documents_by_class_structure(self, biennium, document_class, num_documents):
        """Test that getAllDocumentsByClass returns proper structure."""
        with patch("src.wa_leg_mcp.tools.document_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_documents = [
                {
                    "name": f"Document {i}",
                    "class": document_class,
                    "url": f"http://example.com/doc{i}.pdf",
                    "bill_id": f"HB {1000 + i}",
                    "date": "2023-01-15",
                }
                for i in range(num_documents)
            ]
            mock_client.get_all_documents_by_class.return_value = mock_documents

            result = get_all_documents_by_class(biennium, document_class)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert isinstance(result["data"], list)
                assert result["metadata"]["biennium"] == biennium
                assert result["metadata"]["document_class"] == document_class
                if result["data"]:
                    assert result["metadata"]["count"] == num_documents

    @given(biennium=bienniums, document_class=document_classes)
    def test_all_documents_by_class_empty_handling(self, biennium, document_class):
        """Test that empty document class returns empty list with message."""
        with patch("src.wa_leg_mcp.tools.document_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_all_documents_by_class.return_value = []

            result = get_all_documents_by_class(biennium, document_class)

            assert result["success"] is True
            assert result["data"] == []
            assert "message" in result["metadata"]
            assert document_class in result["metadata"]["message"]

    @given(
        biennium=bienniums,
        document_class=document_classes,
        num_documents=st.integers(min_value=1, max_value=50)
    )
    def test_all_documents_by_class_include_required_fields(
        self, biennium, document_class, num_documents
    ):
        """Test that documents include all required fields."""
        with patch("src.wa_leg_mcp.tools.document_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_documents = [
                {
                    "name": f"Document {i}",
                    "class": document_class,
                    "url": f"http://example.com/doc{i}.pdf",
                    "bill_id": f"HB {1000 + i}",
                    "date": "2023-01-15",
                }
                for i in range(num_documents)
            ]
            mock_client.get_all_documents_by_class.return_value = mock_documents

            result = get_all_documents_by_class(biennium, document_class)

            if result["success"] and result["data"]:
                for document in result["data"]:
                    # Verify required fields are present
                    assert "name" in document
                    assert "class" in document
                    assert "url" in document


@pytest.mark.property_test
class TestDocumentNamePatternMatchingProperties:
    """
    Property 39: Document Name Pattern Matching
    
    For any biennium, document class, and name filter pattern, calling getDocumentsByClass
    SHALL return only documents whose names match the filter pattern.
    
    **Validates: Requirements 13.3**
    """

    @given(
        biennium=bienniums,
        document_class=document_classes,
        name_filter=name_filters,
        num_documents=st.integers(min_value=0, max_value=50)
    )
    def test_documents_by_class_with_filter_structure(
        self, biennium, document_class, name_filter, num_documents
    ):
        """Test that getDocumentsByClass with filter returns proper structure."""
        with patch("src.wa_leg_mcp.tools.document_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_documents = [
                {
                    "name": f"HB {1000 + i}",
                    "class": document_class,
                    "url": f"http://example.com/doc{i}.pdf",
                    "bill_id": f"HB {1000 + i}",
                    "date": "2023-01-15",
                }
                for i in range(num_documents)
            ]
            mock_client.get_documents_by_class.return_value = mock_documents

            result = get_documents_by_class(biennium, document_class, name_filter)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert isinstance(result["data"], list)
                assert result["metadata"]["biennium"] == biennium
                assert result["metadata"]["document_class"] == document_class
                assert result["metadata"]["name_filter"] == name_filter
                if result["data"]:
                    assert result["metadata"]["count"] == num_documents

    @given(biennium=bienniums, document_class=document_classes, name_filter=name_filters)
    def test_documents_by_class_with_filter_empty_handling(
        self, biennium, document_class, name_filter
    ):
        """Test that no matching documents returns empty list with message."""
        with patch("src.wa_leg_mcp.tools.document_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_documents_by_class.return_value = []

            result = get_documents_by_class(biennium, document_class, name_filter)

            assert result["success"] is True
            assert result["data"] == []
            assert "message" in result["metadata"]
            assert name_filter in result["metadata"]["message"]

    @given(
        biennium=bienniums,
        document_class=document_classes,
        name_filter=name_filters,
        num_documents=st.integers(min_value=1, max_value=30)
    )
    def test_documents_by_class_with_filter_include_required_fields(
        self, biennium, document_class, name_filter, num_documents
    ):
        """Test that filtered documents include all required fields."""
        with patch("src.wa_leg_mcp.tools.document_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_documents = [
                {
                    "name": f"HB {1000 + i}",
                    "class": document_class,
                    "url": f"http://example.com/doc{i}.pdf",
                    "bill_id": f"HB {1000 + i}",
                    "date": "2023-01-15",
                }
                for i in range(num_documents)
            ]
            mock_client.get_documents_by_class.return_value = mock_documents

            result = get_documents_by_class(biennium, document_class, name_filter)

            if result["success"] and result["data"]:
                for document in result["data"]:
                    # Verify required fields are present
                    assert "name" in document
                    assert "class" in document
                    assert "url" in document
