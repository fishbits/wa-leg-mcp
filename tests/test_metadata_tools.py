"""
Unit tests for metadata and reference tools.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from src.wa_leg_mcp.tools.metadata_tools import (
    get_committee_meeting_items,
    get_legislation_by_request_number,
    get_legislation_types,
    get_revised_committee_meetings,
)


@pytest.fixture
def mock_wsl_client():
    """Mock WSLClient for testing."""
    with patch("src.wa_leg_mcp.tools.metadata_tools.WSLClient") as mock_class:
        yield mock_class.return_value


@pytest.fixture
def clear_cache():
    """Clear the legislation types cache before each test."""
    import src.wa_leg_mcp.tools.metadata_tools as metadata_tools
    metadata_tools._legislation_types_cache = None
    metadata_tools._cache_timestamp = None
    yield
    metadata_tools._legislation_types_cache = None
    metadata_tools._cache_timestamp = None


class TestGetLegislationTypes:
    """Tests for get_legislation_types function."""

    def test_success_first_call(self, mock_wsl_client, clear_cache):
        """Test successful retrieval on first call (cache miss)."""
        mock_types = [
            {"code": "B", "description": "Bill"},
            {"code": "R", "description": "Resolution"},
        ]
        mock_wsl_client.get_legislation_types.return_value = mock_types

        result = get_legislation_types()

        assert result["success"] is True
        assert len(result["data"]) == 2
        assert result["metadata"]["cached"] is False
        assert result["metadata"]["count"] == 2

    def test_cached_response(self, mock_wsl_client, clear_cache):
        """Test that second call returns cached data."""
        mock_types = [{"code": "B", "description": "Bill"}]
        mock_wsl_client.get_legislation_types.return_value = mock_types

        # First call
        result1 = get_legislation_types()
        assert result1["metadata"]["cached"] is False

        # Second call should be cached
        result2 = get_legislation_types()
        assert result2["success"] is True
        assert result2["metadata"]["cached"] is True
        assert "cache_age_seconds" in result2["metadata"]

        # API should only be called once
        assert mock_wsl_client.get_legislation_types.call_count == 1

    def test_cache_expiration(self, mock_wsl_client, clear_cache):
        """Test that cache expires after TTL."""
        import src.wa_leg_mcp.tools.metadata_tools as metadata_tools
        
        mock_types = [{"code": "B", "description": "Bill"}]
        mock_wsl_client.get_legislation_types.return_value = mock_types

        # First call
        get_legislation_types()

        # Manually expire cache
        metadata_tools._cache_timestamp = datetime.now() - timedelta(hours=25)

        # Second call should fetch fresh data
        result = get_legislation_types()
        assert result["metadata"]["cached"] is False
        assert mock_wsl_client.get_legislation_types.call_count == 2

    def test_api_failure_with_cache(self, mock_wsl_client, clear_cache):
        """Test that stale cache is returned on API failure."""
        import src.wa_leg_mcp.tools.metadata_tools as metadata_tools
        
        mock_types = [{"code": "B", "description": "Bill"}]
        mock_wsl_client.get_legislation_types.return_value = mock_types

        # First call succeeds
        get_legislation_types()

        # Second call fails but returns cached data
        mock_wsl_client.get_legislation_types.return_value = None
        metadata_tools._cache_timestamp = datetime.now() - timedelta(hours=25)

        result = get_legislation_types()
        assert result["success"] is True
        assert result["metadata"]["cached"] is True
        assert result["metadata"]["stale"] is True
        assert "warning" in result["metadata"]

    def test_api_failure_no_cache(self, mock_wsl_client, clear_cache):
        """Test API failure with no cached data."""
        mock_wsl_client.get_legislation_types.return_value = None

        result = get_legislation_types()

        assert result["success"] is False
        assert "no cached data available" in result["error"]

    def test_empty_result(self, mock_wsl_client, clear_cache):
        """Test handling of empty result."""
        mock_wsl_client.get_legislation_types.return_value = []

        result = get_legislation_types()

        assert result["success"] is True
        assert result["data"] == []
        assert "No legislation types found" in result["metadata"]["message"]


class TestGetLegislationByRequestNumber:
    """Tests for get_legislation_by_request_number function."""

    def test_success(self, mock_wsl_client):
        """Test successful retrieval by request number."""
        mock_legislation = {
            "bill_id": "HB 1234",
            "request_number": "23-1234",
            "title": "Test Bill",
        }
        mock_wsl_client.get_legislation_by_request_number.return_value = mock_legislation

        result = get_legislation_by_request_number("2023-24", "23-1234")

        assert result["success"] is True
        assert result["data"]["bill_id"] == "HB 1234"
        assert result["metadata"]["request_number"] == "23-1234"

    def test_not_found(self, mock_wsl_client):
        """Test handling of request number not found."""
        mock_wsl_client.get_legislation_by_request_number.return_value = {}

        result = get_legislation_by_request_number("2023-24", "99-9999")

        assert result["success"] is True
        assert result["data"] == {}
        assert "No legislation found" in result["metadata"]["message"]
        assert "pending or invalid" in result["metadata"]["message"]

    def test_invalid_request_number(self, mock_wsl_client):
        """Test with invalid request number format."""
        result = get_legislation_by_request_number("2023-24", "")

        assert result["success"] is False
        assert "Invalid request number format" in result["error"]

    def test_api_failure(self, mock_wsl_client):
        """Test handling of API failure."""
        mock_wsl_client.get_legislation_by_request_number.return_value = None

        result = get_legislation_by_request_number("2023-24", "23-1234")

        assert result["success"] is False
        assert "Failed to retrieve legislation" in result["error"]


class TestGetCommitteeMeetingItems:
    """Tests for get_committee_meeting_items function."""

    def test_success(self, mock_wsl_client):
        """Test successful retrieval of meeting items."""
        mock_items = [
            {"bill_id": "HB 1000", "topic": "Public hearing"},
            {"bill_id": "SB 5000", "topic": "Executive session"},
        ]
        mock_wsl_client.get_committee_meeting_items.return_value = mock_items

        result = get_committee_meeting_items(12345)

        assert result["success"] is True
        assert len(result["data"]) == 2
        assert result["metadata"]["count"] == 2
        assert result["metadata"]["meeting_id"] == 12345

    def test_empty(self, mock_wsl_client):
        """Test handling of meeting with no items."""
        mock_wsl_client.get_committee_meeting_items.return_value = []

        result = get_committee_meeting_items(12345)

        assert result["success"] is True
        assert result["data"] == []
        assert "No agenda items found" in result["metadata"]["message"]

    def test_invalid_meeting_id(self, mock_wsl_client):
        """Test with invalid meeting ID."""
        result = get_committee_meeting_items(-1)

        assert result["success"] is False
        assert "Invalid meeting ID" in result["error"]

    def test_api_failure(self, mock_wsl_client):
        """Test handling of API failure."""
        mock_wsl_client.get_committee_meeting_items.return_value = None

        result = get_committee_meeting_items(12345)

        assert result["success"] is False
        assert "Failed to retrieve meeting items" in result["error"]


class TestGetRevisedCommitteeMeetings:
    """Tests for get_revised_committee_meetings function."""

    def test_success(self, mock_wsl_client):
        """Test successful retrieval of revised meetings."""
        mock_meetings = [
            {"agenda_id": 1, "date": "2023-02-15", "revised": True},
            {"agenda_id": 2, "date": "2023-02-16", "revised": True},
        ]
        mock_wsl_client.get_revised_committee_meetings.return_value = mock_meetings

        result = get_revised_committee_meetings("2023-01-01")

        assert result["success"] is True
        assert len(result["data"]) == 2
        assert result["metadata"]["count"] == 2
        assert result["metadata"]["since_date"] == "2023-01-01"

    def test_with_biennium_filter(self, mock_wsl_client):
        """Test filtering by biennium."""
        mock_meetings = [
            {"agenda_id": 1, "biennium": "2023-24", "revised": True},
            {"agenda_id": 2, "biennium": "2021-22", "revised": True},
        ]
        mock_wsl_client.get_revised_committee_meetings.return_value = mock_meetings

        result = get_revised_committee_meetings("2023-01-01", "2023-24")

        assert result["success"] is True
        assert len(result["data"]) == 1
        assert result["data"][0]["biennium"] == "2023-24"

    def test_empty(self, mock_wsl_client):
        """Test handling of no revised meetings."""
        mock_wsl_client.get_revised_committee_meetings.return_value = []

        result = get_revised_committee_meetings("2023-01-01")

        assert result["success"] is True
        assert result["data"] == []
        assert "No revised meetings found" in result["metadata"]["message"]

    def test_invalid_date_format(self, mock_wsl_client):
        """Test with invalid date format."""
        result = get_revised_committee_meetings("invalid-date")

        assert result["success"] is False
        assert "Invalid date format" in result["error"]
        assert "ISO 8601" in result["error"]

    def test_api_failure(self, mock_wsl_client):
        """Test handling of API failure."""
        mock_wsl_client.get_revised_committee_meetings.return_value = None

        result = get_revised_committee_meetings("2023-01-01")

        assert result["success"] is False
        assert "Failed to retrieve revised meetings" in result["error"]
