"""
Unit tests for session law tools.
"""

import pytest
from unittest.mock import MagicMock, patch

from src.wa_leg_mcp.tools.session_law_tools import (
    get_session_law_by_bill,
    get_session_law_by_bill_id,
    get_bill_by_chapter_number,
    get_chapter_numbers_by_year,
    get_session_law_by_initiative_number,
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



class TestGetSessionLawByBillId:
    """Tests for get_session_law_by_bill_id function."""

    def test_get_session_law_by_bill_id_success(self, mock_wsl_client):
        """Test successful session law retrieval by bill ID."""
        mock_session_law = {
            "chapter": "456",
            "year": 2023,
            "session": "Regular",
            "effective_date": "2023-08-01",
            "law_text_url": "http://example.com/law.pdf",
            "multiple_effective_dates": False,
            "partial_veto": False,
        }
        mock_wsl_client.get_session_law_by_bill_id.return_value = mock_session_law

        result = get_session_law_by_bill_id("HB 1234", "2023-24")

        assert result["success"] is True
        assert result["data"]["bill_id"] == "HB 1234"
        assert result["data"]["session_law"]["chapter"] == "456"
        mock_wsl_client.get_session_law_by_bill_id.assert_called_once_with("2023-24", "HB 1234")

    def test_get_session_law_by_bill_id_not_enacted(self, mock_wsl_client):
        """Test session law retrieval for bill not enacted."""
        mock_wsl_client.get_session_law_by_bill_id.return_value = None

        result = get_session_law_by_bill_id("SB 9999", "2023-24")

        assert result["success"] is True
        assert result["data"]["session_law"] is None
        assert "not been enacted" in result["metadata"]["message"]

    def test_get_session_law_by_bill_id_empty(self, mock_wsl_client):
        """Test session law retrieval with empty bill ID."""
        result = get_session_law_by_bill_id("", "2023-24")

        assert result["success"] is False
        assert "cannot be empty" in result["error"]


class TestGetBillByChapterNumber:
    """Tests for get_bill_by_chapter_number function."""

    def test_get_bill_by_chapter_number_success(self, mock_wsl_client):
        """Test successful bill retrieval by chapter number."""
        mock_bill = {
            "bill_id": "HB 1234",
            "bill_number": 1234,
            "short_description": "Test bill",
        }
        mock_wsl_client.get_bill_by_chapter_number.return_value = mock_bill

        result = get_bill_by_chapter_number("2023", "123")

        assert result["success"] is True
        assert result["data"]["year"] == "2023"
        assert result["data"]["chapter_number"] == "123"
        assert result["data"]["bill"]["bill_id"] == "HB 1234"
        mock_wsl_client.get_bill_by_chapter_number.assert_called_once_with(2023, 0, 123)

    def test_get_bill_by_chapter_number_with_session(self, mock_wsl_client):
        """Test bill retrieval with special session."""
        mock_bill = {"bill_id": "SB 5678"}
        mock_wsl_client.get_bill_by_chapter_number.return_value = mock_bill

        result = get_bill_by_chapter_number("2023", "456", session=1)

        assert result["success"] is True
        assert result["data"]["session"] == 1
        mock_wsl_client.get_bill_by_chapter_number.assert_called_once_with(2023, 1, 456)

    def test_get_bill_by_chapter_number_not_found(self, mock_wsl_client):
        """Test bill retrieval when chapter not found."""
        mock_wsl_client.get_bill_by_chapter_number.return_value = None

        result = get_bill_by_chapter_number("2023", "999")

        assert result["success"] is True
        assert result["data"]["bill"] is None
        assert "No bill found" in result["metadata"]["message"]

    def test_get_bill_by_chapter_number_invalid_year(self, mock_wsl_client):
        """Test bill retrieval with invalid year."""
        result = get_bill_by_chapter_number("23", "123")

        assert result["success"] is False
        assert "Invalid year format" in result["error"]

    def test_get_bill_by_chapter_number_invalid_chapter(self, mock_wsl_client):
        """Test bill retrieval with invalid chapter number."""
        result = get_bill_by_chapter_number("2023", "ABC")

        assert result["success"] is False
        assert "Invalid chapter number format" in result["error"]


class TestGetChapterNumbersByYear:
    """Tests for get_chapter_numbers_by_year function."""

    def test_get_chapter_numbers_by_year_success(self, mock_wsl_client):
        """Test successful chapter numbers retrieval."""
        mock_chapters = [
            {"chapter": "1", "bill_id": "HB 1001"},
            {"chapter": "2", "bill_id": "SB 5001"},
        ]
        mock_wsl_client.get_chapter_numbers_by_year.return_value = mock_chapters

        result = get_chapter_numbers_by_year("2023")

        assert result["success"] is True
        assert result["data"]["year"] == "2023"
        assert len(result["data"]["chapters"]) == 2
        assert result["metadata"]["count"] == 2
        mock_wsl_client.get_chapter_numbers_by_year.assert_called_once_with(2023)

    def test_get_chapter_numbers_by_year_empty(self, mock_wsl_client):
        """Test chapter numbers retrieval with no results."""
        mock_wsl_client.get_chapter_numbers_by_year.return_value = []

        result = get_chapter_numbers_by_year("2023")

        assert result["success"] is True
        assert result["data"]["chapters"] == []
        assert result["metadata"]["count"] == 0

    def test_get_chapter_numbers_by_year_invalid_year(self, mock_wsl_client):
        """Test chapter numbers retrieval with invalid year."""
        result = get_chapter_numbers_by_year("23")

        assert result["success"] is False
        assert "Invalid year format" in result["error"]


class TestGetSessionLawByInitiativeNumber:
    """Tests for get_session_law_by_initiative_number function."""

    def test_get_session_law_by_initiative_number_success(self, mock_wsl_client):
        """Test successful session law retrieval for initiative."""
        mock_session_law = {
            "chapter": "50",
            "year": 2023,
            "session": "Regular",
            "effective_date": "2023-12-07",
            "law_text_url": "http://example.com/initiative.pdf",
            "multiple_effective_dates": False,
            "partial_veto": False,
        }
        mock_wsl_client.get_session_law_by_initiative_number.return_value = mock_session_law

        result = get_session_law_by_initiative_number("1234")

        assert result["success"] is True
        assert result["data"]["initiative_number"] == "1234"
        assert result["data"]["session_law"]["chapter"] == "50"
        mock_wsl_client.get_session_law_by_initiative_number.assert_called_once_with(1234)

    def test_get_session_law_by_initiative_number_not_enacted(self, mock_wsl_client):
        """Test session law retrieval for initiative not enacted."""
        mock_wsl_client.get_session_law_by_initiative_number.return_value = None

        result = get_session_law_by_initiative_number("9999")

        assert result["success"] is True
        assert result["data"]["session_law"] is None
        assert "not been enacted" in result["metadata"]["message"]

    def test_get_session_law_by_initiative_number_invalid(self, mock_wsl_client):
        """Test session law retrieval with invalid initiative number."""
        result = get_session_law_by_initiative_number("ABC")

        assert result["success"] is False
        assert "Invalid initiative number format" in result["error"]
