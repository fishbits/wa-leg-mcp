"""
Unit tests for session law tools.
"""

import pytest
from unittest.mock import MagicMock, patch

from src.wa_leg_mcp.tools.session_law_tools import (
    get_session_law_by_bill,
)


@pytest.fixture
def mock_wsl_client():
    """Mock WSLClient for testing."""
    with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock:
        yield mock


class TestGetSessionLawByBill:
    """Tests for get_session_law_by_bill function."""

    def test_get_session_law_by_bill_success(self, mock_wsl_client):
        """Test successful session law retrieval."""
        # Mock session law data
        mock_session_law = {
            "chapter": "123",
            "year": 2023,
            "session": "Regular",
            "effective_date": "2023-07-23",
            "law_text_url": "http://example.com/law.pdf",
            "multiple_effective_dates": False,
            "partial_veto": False,
        }
        mock_wsl_client.get_session_law_by_bill.return_value = mock_session_law

        result = get_session_law_by_bill("HB 1234", "2023-24")

        assert result["success"] is True
        assert result["data"]["bill_number"] == "HB 1234"
        assert result["data"]["biennium"] == "2023-24"
        assert result["data"]["session_law"]["chapter"] == "123"
        assert result["data"]["session_law"]["year"] == "2023"
        assert result["data"]["session_law"]["effective_date"] == "2023-07-23"
        mock_wsl_client.get_session_law_by_bill.assert_called_once_with("2023-24", 1234)

    def test_get_session_law_by_bill_numeric_only(self, mock_wsl_client):
        """Test session law retrieval with numeric bill number."""
        mock_session_law = {
            "chapter": "456",
            "year": 2023,
            "session": "Regular",
            "effective_date": "2023-08-01",
            "law_text_url": "http://example.com/law2.pdf",
            "multiple_effective_dates": False,
            "partial_veto": False,
        }
        mock_wsl_client.get_session_law_by_bill.return_value = mock_session_law

        result = get_session_law_by_bill("5678", "2023-24")

        assert result["success"] is True
        assert result["data"]["session_law"]["chapter"] == "456"
        mock_wsl_client.get_session_law_by_bill.assert_called_once_with("2023-24", 5678)

    def test_get_session_law_by_bill_not_enacted(self, mock_wsl_client):
        """Test session law retrieval for bill not enacted into law."""
        mock_wsl_client.get_session_law_by_bill.return_value = None

        result = get_session_law_by_bill("HB 9999", "2023-24")

        assert result["success"] is True
        assert result["data"]["session_law"] is None
        assert "not been enacted" in result["metadata"]["message"]

    def test_get_session_law_by_bill_invalid_bill_number(self, mock_wsl_client):
        """Test session law retrieval with invalid bill number."""
        result = get_session_law_by_bill("INVALID", "2023-24")

        assert result["success"] is False
        assert "Invalid bill number format" in result["error"]
        assert result["error_type"] == "validation"

    def test_get_session_law_by_bill_empty_bill_number(self, mock_wsl_client):
        """Test session law retrieval with empty bill number."""
        result = get_session_law_by_bill("", "2023-24")

        assert result["success"] is False
        assert "Invalid bill number format" in result["error"]

    def test_get_session_law_by_bill_default_biennium(self, mock_wsl_client):
        """Test session law retrieval with default biennium."""
        mock_session_law = {
            "chapter": "789",
            "year": 2025,
            "session": "Regular",
            "effective_date": "2025-07-01",
            "law_text_url": "http://example.com/law3.pdf",
            "multiple_effective_dates": False,
            "partial_veto": False,
        }
        mock_wsl_client.get_session_law_by_bill.return_value = mock_session_law

        with patch("src.wa_leg_mcp.tools.session_law_tools.get_current_biennium") as mock_biennium:
            mock_biennium.return_value = "2025-26"
            result = get_session_law_by_bill("HB 1111")

        assert result["success"] is True
        assert result["data"]["biennium"] == "2025-26"

    def test_get_session_law_by_bill_with_multiple_effective_dates(self, mock_wsl_client):
        """Test session law retrieval with multiple effective dates."""
        mock_session_law = {
            "chapter": "200",
            "year": 2023,
            "session": "Regular",
            "effective_date": "2023-07-23",
            "law_text_url": "http://example.com/law4.pdf",
            "multiple_effective_dates": True,
            "partial_veto": False,
        }
        mock_wsl_client.get_session_law_by_bill.return_value = mock_session_law

        result = get_session_law_by_bill("HB 2222", "2023-24")

        assert result["success"] is True
        assert result["data"]["session_law"]["multiple_effective_dates"] is True

    def test_get_session_law_by_bill_with_partial_veto(self, mock_wsl_client):
        """Test session law retrieval with partial veto."""
        mock_session_law = {
            "chapter": "300",
            "year": 2023,
            "session": "Regular",
            "effective_date": "2023-07-23",
            "law_text_url": "http://example.com/law5.pdf",
            "multiple_effective_dates": False,
            "partial_veto": True,
        }
        mock_wsl_client.get_session_law_by_bill.return_value = mock_session_law

        result = get_session_law_by_bill("HB 3333", "2023-24")

        assert result["success"] is True
        assert result["data"]["session_law"]["partial_veto"] is True

    def test_get_session_law_by_bill_api_error(self, mock_wsl_client):
        """Test session law retrieval with API error."""
        mock_wsl_client.get_session_law_by_bill.side_effect = Exception("API connection failed")

        result = get_session_law_by_bill("HB 1234", "2023-24")

        assert result["success"] is False
        assert "Failed to fetch session law" in result["error"]
        assert result["error_type"] == "unexpected"
