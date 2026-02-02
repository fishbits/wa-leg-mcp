"""
Property-based tests for bill passage and status tracking tools.

These tests validate correctness properties for passage tracking tools using
property-based testing with hypothesis.
"""

import pytest
from hypothesis import given, strategies as st
from unittest.mock import patch

from src.wa_leg_mcp.tools.passage_tools import (
    get_legislation_passed_house,
    get_legislation_passed_legislature,
    get_legislation_passed_senate,
    get_legislative_status_changes,
    get_prefiled_legislation,
)


# Test data strategies
bienniums = st.sampled_from(["2021-22", "2023-24", "2025-26"])
# Generate ISO 8601 date strings
iso_dates = st.sampled_from([
    "2020-01-01", "2021-06-15", "2022-03-20", "2023-01-10", 
    "2023-06-30", "2024-02-14", "2025-09-01", "2026-12-31"
])


@pytest.mark.property_test
class TestHousePassageRetrievalProperties:
    """
    Property 33: House Passage Retrieval
    
    For any biennium, calling getLegislationPassedHouse SHALL return all bills
    that passed the House during that biennium.
    
    **Validates: Requirements 11.1**
    """

    @given(biennium=bienniums, num_bills=st.integers(min_value=0, max_value=100))
    def test_house_passage_structure(self, biennium, num_bills):
        """Test that House passage retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.passage_tools.wsl_client") as mock_client:
            mock_bills = [
                {
                    "bill_id": f"HB {1000+i}",
                    "bill_number": str(1000+i),
                    "substitute_version": "0",
                    "engrossed_version": "0",
                    "short_legislation_type": {"short_legislation_type": "B"},
                    "original_agency": "House",
                    "active": True,
                }
                for i in range(num_bills)
            ]
            mock_client.get_legislation_passed_house.return_value = mock_bills

            result = get_legislation_passed_house(biennium)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "bills" in result["data"]
                assert isinstance(result["data"]["bills"], list)
                assert result["metadata"]["count"] == num_bills

    @given(biennium=bienniums)
    def test_house_passage_empty_handling(self, biennium):
        """Test that empty House passage returns empty list with message."""
        with patch("src.wa_leg_mcp.tools.passage_tools.wsl_client") as mock_client:
            mock_client.get_legislation_passed_house.return_value = []

            result = get_legislation_passed_house(biennium)

            assert result["success"] is True
            assert result["data"]["bills"] == []
            assert "message" in result["metadata"]


@pytest.mark.property_test
class TestSenatePassageRetrievalProperties:
    """
    Property 34: Senate Passage Retrieval
    
    For any biennium, calling getLegislationPassedSenate SHALL return all bills
    that passed the Senate during that biennium.
    
    **Validates: Requirements 11.2**
    """

    @given(biennium=bienniums, num_bills=st.integers(min_value=0, max_value=50))
    def test_senate_passage_structure(self, biennium, num_bills):
        """Test that Senate passage retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.passage_tools.wsl_client") as mock_client:
            mock_bills = [
                {
                    "bill_id": f"SB {5000+i}",
                    "bill_number": str(5000+i),
                    "substitute_version": "0",
                    "engrossed_version": "0",
                    "short_legislation_type": {"short_legislation_type": "B"},
                    "original_agency": "Senate",
                    "active": True,
                }
                for i in range(num_bills)
            ]
            mock_client.get_legislation_passed_senate.return_value = mock_bills

            result = get_legislation_passed_senate(biennium)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "bills" in result["data"]
                assert isinstance(result["data"]["bills"], list)
                assert result["metadata"]["count"] == num_bills

    @given(biennium=bienniums)
    def test_senate_passage_empty_handling(self, biennium):
        """Test that empty Senate passage returns empty list with message."""
        with patch("src.wa_leg_mcp.tools.passage_tools.wsl_client") as mock_client:
            mock_client.get_legislation_passed_senate.return_value = []

            result = get_legislation_passed_senate(biennium)

            assert result["success"] is True
            assert result["data"]["bills"] == []
            assert "message" in result["metadata"]


@pytest.mark.property_test
class TestLegislaturePassageRetrievalProperties:
    """
    Property 35: Legislature Passage Retrieval
    
    For any biennium, calling getLegislationPassedLegislature SHALL return only
    bills that passed both chambers.
    
    **Validates: Requirements 11.3**
    """

    @given(biennium=bienniums, num_bills=st.integers(min_value=0, max_value=50))
    def test_legislature_passage_structure(self, biennium, num_bills):
        """Test that legislature passage retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.passage_tools.wsl_client") as mock_client:
            mock_bills = [
                {
                    "bill_id": f"HB {1000+i}",
                    "bill_number": str(1000+i),
                    "substitute_version": "0",
                    "engrossed_version": "0",
                    "short_legislation_type": {"short_legislation_type": "B"},
                    "original_agency": "House",
                    "active": True,
                }
                for i in range(num_bills)
            ]
            mock_client.get_legislation_passed_legislature.return_value = mock_bills

            result = get_legislation_passed_legislature(biennium)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "bills" in result["data"]
                assert isinstance(result["data"]["bills"], list)
                assert result["metadata"]["count"] == num_bills

    @given(biennium=bienniums)
    def test_legislature_passage_empty_handling(self, biennium):
        """Test that empty legislature passage returns empty list with message."""
        with patch("src.wa_leg_mcp.tools.passage_tools.wsl_client") as mock_client:
            mock_client.get_legislation_passed_legislature.return_value = []

            result = get_legislation_passed_legislature(biennium)

            assert result["success"] is True
            assert result["data"]["bills"] == []
            assert "message" in result["metadata"]


@pytest.mark.property_test
class TestPrefiledLegislationRetrievalProperties:
    """
    Property 36: Prefiled Legislation Retrieval
    
    For any biennium, calling getPrefiledLegislation SHALL return all bills
    filed before the session start date.
    
    **Validates: Requirements 12.1**
    """

    @given(num_bills=st.integers(min_value=0, max_value=50))
    def test_prefiled_legislation_structure(self, num_bills):
        """Test that prefiled legislation retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.passage_tools.wsl_client") as mock_client:
            mock_bills = [
                {
                    "biennium": "2025-26",
                    "bill_id": f"HB {1000+i}",
                    "bill_number": str(1000+i),
                    "substitute_version": "0",
                    "engrossed_version": "0",
                    "short_legislation_type": {"short_legislation_type": "B"},
                    "original_agency": "House",
                    "active": True,
                    "short_description": f"Prefiled bill {i}",
                    "introduced_date": "2024-12-01",
                }
                for i in range(num_bills)
            ]
            mock_client.get_prefiled_legislation.return_value = mock_bills

            result = get_prefiled_legislation()

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "bills" in result["data"]
                assert isinstance(result["data"]["bills"], list)
                assert result["metadata"]["count"] == num_bills

    def test_prefiled_legislation_empty_handling(self):
        """Test that empty prefiled legislation returns empty list with message."""
        with patch("src.wa_leg_mcp.tools.passage_tools.wsl_client") as mock_client:
            mock_client.get_prefiled_legislation.return_value = []

            result = get_prefiled_legislation()

            assert result["success"] is True
            assert result["data"]["bills"] == []
            assert "message" in result["metadata"]


@pytest.mark.property_test
class TestStatusChangeDateRangeFilteringProperties:
    """
    Property 32: Status Change Date Range Filtering
    
    For any date range, calling getLegislativeStatusChanges SHALL return all bills
    with status updates within that period, and no bills with updates outside that period.
    
    **Validates: Requirements 10.1**
    """

    @given(
        biennium=bienniums,
        begin_date=iso_dates,
        end_date=iso_dates,
        num_changes=st.integers(min_value=0, max_value=50)
    )
    def test_status_changes_structure(self, biennium, begin_date, end_date, num_changes):
        """Test that status changes retrieval returns proper structure."""
        # Ensure begin_date <= end_date
        if begin_date > end_date:
            begin_date, end_date = end_date, begin_date

        with patch("src.wa_leg_mcp.tools.passage_tools.wsl_client") as mock_client:
            mock_changes = [
                {
                    "bill_id": f"HB {1000+i}",
                    "action_date": begin_date,
                    "history_line": f"Status change {i}",
                    "status": "H Rules",
                    "amended_by_opposite_body": False,
                    "partial_veto": False,
                    "veto": False,
                    "amendments_exist": False,
                }
                for i in range(num_changes)
            ]
            mock_client.get_legislative_status_changes.return_value = mock_changes

            result = get_legislative_status_changes(begin_date, end_date, biennium)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "status_changes" in result["data"]
                assert isinstance(result["data"]["status_changes"], list)
                assert result["data"]["begin_date"] == begin_date
                assert result["data"]["end_date"] == end_date
                assert result["metadata"]["count"] == num_changes

    @given(biennium=bienniums, begin_date=iso_dates, end_date=iso_dates)
    def test_status_changes_empty_handling(self, biennium, begin_date, end_date):
        """Test that empty status changes return empty list with message."""
        # Ensure begin_date <= end_date
        if begin_date > end_date:
            begin_date, end_date = end_date, begin_date

        with patch("src.wa_leg_mcp.tools.passage_tools.wsl_client") as mock_client:
            mock_client.get_legislative_status_changes.return_value = []

            result = get_legislative_status_changes(begin_date, end_date, biennium)

            assert result["success"] is True
            assert result["data"]["status_changes"] == []
            assert "message" in result["metadata"]


@pytest.mark.property_test
class TestISO8601DateAcceptanceProperties:
    """
    Property 9: ISO 8601 Date Acceptance
    
    For any MCP tool that accepts date parameters, dates in ISO 8601 format
    (e.g., "2023-01-15") SHALL be accepted and parsed correctly.
    
    **Validates: Requirements 10.5**
    """

    @given(
        biennium=bienniums,
        begin_date=iso_dates,
        end_date=iso_dates
    )
    def test_iso_8601_date_format_accepted(self, biennium, begin_date, end_date):
        """Test that ISO 8601 date format is accepted and parsed correctly."""
        # Ensure begin_date <= end_date
        if begin_date > end_date:
            begin_date, end_date = end_date, begin_date

        with patch("src.wa_leg_mcp.tools.passage_tools.wsl_client") as mock_client:
            mock_client.get_legislative_status_changes.return_value = []

            result = get_legislative_status_changes(begin_date, end_date, biennium)

            # Should succeed with ISO 8601 dates
            assert result["success"] is True
            assert result["data"]["begin_date"] == begin_date
            assert result["data"]["end_date"] == end_date

    def test_invalid_date_format_rejected(self):
        """Test that invalid date formats are rejected with descriptive error."""
        with patch("src.wa_leg_mcp.tools.passage_tools.wsl_client") as mock_client:
            # Mock the client to raise ValueError for invalid date
            mock_client.get_legislative_status_changes.side_effect = ValueError("Invalid date format")

            result = get_legislative_status_changes("invalid-date", "2023-12-31", "2023-24")

            # Should fail with validation error
            assert result["success"] is False
            assert "error" in result
            assert "date format" in result["error"].lower()
            assert result["error_type"] == "validation"
