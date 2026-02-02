"""
Property-based tests for metadata and reference tools.

These tests validate correctness properties for metadata tools using
property-based testing with hypothesis.
"""

import pytest
from datetime import datetime, timedelta
from hypothesis import given, strategies as st
from unittest.mock import patch

from src.wa_leg_mcp.tools.metadata_tools import (
    get_committee_meeting_items,
    get_legislation_by_request_number,
    get_legislation_types,
    get_revised_committee_meetings,
)


# Test data strategies
bienniums = st.sampled_from(["2021-22", "2023-24", "2025-26"])
request_numbers = st.sampled_from(["21-1234", "23-5678", "25-9999"])
meeting_ids = st.integers(min_value=1, max_value=99999)
dates = st.sampled_from(["2021-01-01", "2023-06-15", "2025-12-31"])


@pytest.fixture
def clear_cache():
    """Clear the legislation types cache before each test."""
    import src.wa_leg_mcp.tools.metadata_tools as metadata_tools
    metadata_tools._legislation_types_cache = None
    metadata_tools._cache_timestamp = None
    yield
    metadata_tools._legislation_types_cache = None
    metadata_tools._cache_timestamp = None


@pytest.mark.property_test
class TestLegislationTypeRetrievalProperties:
    """
    Property 40: Legislation Type Retrieval
    
    For any call to getLegislationTypes, the response SHALL include all valid
    legislation type codes with descriptions and chamber applicability.
    
    **Validates: Requirements 14.1**
    """

    @given(num_types=st.integers(min_value=0, max_value=20))
    def test_legislation_types_structure(self, num_types):
        """Test that legislation types retrieval returns proper structure."""
        # Clear cache before test
        import src.wa_leg_mcp.tools.metadata_tools as metadata_tools
        metadata_tools._legislation_types_cache = None
        metadata_tools._cache_timestamp = None
        
        with patch("src.wa_leg_mcp.tools.metadata_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_types = [
                {
                    "code": f"T{i}",
                    "description": f"Type {i}",
                    "chamber": "House" if i % 2 == 0 else "Senate",
                }
                for i in range(num_types)
            ]
            mock_client.get_legislation_types.return_value = mock_types

            result = get_legislation_types()

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"] and result["data"]:
                assert isinstance(result["data"], list)
                if not result["metadata"].get("cached"):
                    assert result["metadata"]["count"] == num_types

    @given(num_types=st.integers(min_value=1, max_value=15))
    def test_legislation_types_include_required_fields(self, num_types):
        """Test that legislation types include all required fields."""
        # Clear cache before test
        import src.wa_leg_mcp.tools.metadata_tools as metadata_tools
        metadata_tools._legislation_types_cache = None
        metadata_tools._cache_timestamp = None
        
        with patch("src.wa_leg_mcp.tools.metadata_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_types = [
                {
                    "code": f"T{i}",
                    "description": f"Type {i}",
                }
                for i in range(num_types)
            ]
            mock_client.get_legislation_types.return_value = mock_types

            result = get_legislation_types()

            if result["success"] and result["data"]:
                for leg_type in result["data"]:
                    # Verify required fields are present
                    assert "code" in leg_type
                    assert "description" in leg_type


@pytest.mark.property_test
class TestLegislationTypeCachingProperties:
    """
    Property 41: Legislation Type Caching
    
    For any sequence of calls to getLegislationTypes within 24 hours, only the first
    call SHALL make an API request, and subsequent calls SHALL return cached data
    with cache metadata.
    
    **Validates: Requirements 14.3, 18.1, 18.5**
    """

    def test_caching_behavior(self):
        """Test that caching works correctly."""
        # Clear cache before test
        import src.wa_leg_mcp.tools.metadata_tools as metadata_tools
        metadata_tools._legislation_types_cache = None
        metadata_tools._cache_timestamp = None
        
        with patch("src.wa_leg_mcp.tools.metadata_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_types = [{"code": "B", "description": "Bill"}]
            mock_client.get_legislation_types.return_value = mock_types

            # First call should not be cached
            result1 = get_legislation_types()
            assert result1["success"] is True
            assert result1["metadata"]["cached"] is False

            # Second call should be cached
            result2 = get_legislation_types()
            assert result2["success"] is True
            assert result2["metadata"]["cached"] is True
            assert "cache_age_seconds" in result2["metadata"]

            # API should only be called once
            assert mock_client.get_legislation_types.call_count == 1

    def test_cache_metadata_present(self):
        """Test that cache metadata is present in cached responses."""
        # Clear cache before test
        import src.wa_leg_mcp.tools.metadata_tools as metadata_tools
        metadata_tools._legislation_types_cache = None
        metadata_tools._cache_timestamp = None
        
        with patch("src.wa_leg_mcp.tools.metadata_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_types = [{"code": "B", "description": "Bill"}]
            mock_client.get_legislation_types.return_value = mock_types

            # First call
            get_legislation_types()

            # Second call should have cache metadata
            result = get_legislation_types()
            assert result["metadata"]["cached"] is True
            assert "cache_timestamp" in result["metadata"]
            assert "cache_age_seconds" in result["metadata"]


@pytest.mark.property_test
class TestRequestNumberLookupProperties:
    """
    Property 43: Request Number Lookup
    
    For any valid request number and biennium, calling getLegislationByRequestNumber
    SHALL return the corresponding bill information or pending request status.
    
    **Validates: Requirements 15.1, 15.2**
    """

    @given(biennium=bienniums, request_number=request_numbers)
    def test_request_number_lookup_structure(self, biennium, request_number):
        """Test that request number lookup returns proper structure."""
        with patch("src.wa_leg_mcp.tools.metadata_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_legislation = {
                "bill_id": "HB 1234",
                "request_number": request_number,
                "title": "Test Bill",
            }
            mock_client.get_legislation_by_request_number.return_value = mock_legislation

            result = get_legislation_by_request_number(biennium, request_number)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert result["metadata"]["biennium"] == biennium
                assert result["metadata"]["request_number"] == request_number

    @given(biennium=bienniums, request_number=request_numbers)
    def test_request_number_not_found_handling(self, biennium, request_number):
        """Test that not found request numbers return appropriate message."""
        with patch("src.wa_leg_mcp.tools.metadata_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_legislation_by_request_number.return_value = {}

            result = get_legislation_by_request_number(biennium, request_number)

            assert result["success"] is True
            assert result["data"] == {}
            assert "message" in result["metadata"]
            assert "pending or invalid" in result["metadata"]["message"]


@pytest.mark.property_test
class TestCommitteeMeetingItemsProperties:
    """
    Property tests for committee meeting items retrieval.
    
    **Validates: Requirements 3.2**
    """

    @given(meeting_id=meeting_ids, num_items=st.integers(min_value=0, max_value=50))
    def test_meeting_items_structure(self, meeting_id, num_items):
        """Test that meeting items retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.metadata_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_items = [
                {
                    "bill_id": f"HB {1000 + i}",
                    "topic": f"Topic {i}",
                }
                for i in range(num_items)
            ]
            mock_client.get_committee_meeting_items.return_value = mock_items

            result = get_committee_meeting_items(meeting_id)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert isinstance(result["data"], list)
                assert result["metadata"]["meeting_id"] == meeting_id
                if result["data"]:
                    assert result["metadata"]["count"] == num_items

    @given(meeting_id=meeting_ids)
    def test_meeting_items_empty_handling(self, meeting_id):
        """Test that meetings with no items return empty list with message."""
        with patch("src.wa_leg_mcp.tools.metadata_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_committee_meeting_items.return_value = []

            result = get_committee_meeting_items(meeting_id)

            assert result["success"] is True
            assert result["data"] == []
            assert "message" in result["metadata"]


@pytest.mark.property_test
class TestRevisedCommitteeMeetingsProperties:
    """
    Property tests for revised committee meetings retrieval.
    
    **Validates: Requirements 3.5, 10.5**
    """

    @given(since_date=dates, num_meetings=st.integers(min_value=0, max_value=30))
    def test_revised_meetings_structure(self, since_date, num_meetings):
        """Test that revised meetings retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.metadata_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_meetings = [
                {
                    "agenda_id": i,
                    "date": since_date,
                    "revised": True,
                }
                for i in range(num_meetings)
            ]
            mock_client.get_revised_committee_meetings.return_value = mock_meetings

            result = get_revised_committee_meetings(since_date)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert isinstance(result["data"], list)
                assert result["metadata"]["since_date"] == since_date
                if result["data"]:
                    assert result["metadata"]["count"] == num_meetings

    @given(since_date=dates, biennium=bienniums)
    def test_revised_meetings_biennium_filter(self, since_date, biennium):
        """Test that biennium filter works correctly."""
        with patch("src.wa_leg_mcp.tools.metadata_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_meetings = [
                {"agenda_id": 1, "biennium": biennium, "revised": True},
                {"agenda_id": 2, "biennium": "2019-20", "revised": True},
            ]
            mock_client.get_revised_committee_meetings.return_value = mock_meetings

            result = get_revised_committee_meetings(since_date, biennium)

            if result["success"] and result["data"]:
                # All returned meetings should match the biennium filter
                for meeting in result["data"]:
                    assert meeting["biennium"] == biennium

    @given(since_date=dates)
    def test_revised_meetings_empty_handling(self, since_date):
        """Test that no revised meetings returns empty list with message."""
        with patch("src.wa_leg_mcp.tools.metadata_tools.WSLClient") as mock_client_class:
            mock_client = mock_client_class.return_value
            mock_client.get_revised_committee_meetings.return_value = []

            result = get_revised_committee_meetings(since_date)

            assert result["success"] is True
            assert result["data"] == []
            assert "message" in result["metadata"]
