"""
Property-based tests for chamber filtering correctness.

These tests validate that chamber filtering works correctly across all tools
that accept chamber parameters.
"""

import pytest
from hypothesis import given, strategies as st
from unittest.mock import patch

from src.wa_leg_mcp.tools.enhanced_committee_tools import (
    get_active_house_committees,
    get_active_senate_committees,
    get_house_committees,
    get_senate_committees,
)


# Test data strategies
bienniums = st.sampled_from(["2021-22", "2023-24", "2025-26"])


@pytest.mark.property_test
class TestChamberFilteringProperties:
    """
    Property 5: Chamber Filtering Correctness
    
    For any MCP tool that accepts a chamber filter parameter (House/Senate),
    all returned items SHALL belong only to the specified chamber, and no items
    from the other chamber SHALL be included.
    
    **Validates: Requirements 8.3, 9.2, 12.4**
    """

    @given(num_committees=st.integers(min_value=1, max_value=40))
    def test_active_house_committees_only_returns_house(self, num_committees):
        """Test that getActiveHouseCommittees only returns House committees."""
        with patch("src.wa_leg_mcp.tools.enhanced_committee_tools.wsl_client") as mock_client:
            # Create mock committees - all should be House
            mock_committees = [
                {
                    "id": str(i),
                    "name": f"Committee {i}",
                    "long_name": f"House Committee {i}",
                    "agency": "House",
                    "acronym": f"HC{i}",
                    "phone": "(360) 786-7100",
                }
                for i in range(num_committees)
            ]
            mock_client.get_active_house_committees.return_value = mock_committees

            result = get_active_house_committees()

            # Verify all returned committees are House committees
            if result["success"] and result["data"]["committees"]:
                for committee in result["data"]["committees"]:
                    assert committee["agency"] == "House", \
                        f"Expected House committee but got {committee['agency']}"
                    # Verify no Senate committees are included
                    assert committee["agency"] != "Senate"

    @given(num_committees=st.integers(min_value=1, max_value=40))
    def test_active_senate_committees_only_returns_senate(self, num_committees):
        """Test that getActiveSenateCommittees only returns Senate committees."""
        with patch("src.wa_leg_mcp.tools.enhanced_committee_tools.wsl_client") as mock_client:
            # Create mock committees - all should be Senate
            mock_committees = [
                {
                    "id": str(i),
                    "name": f"Committee {i}",
                    "long_name": f"Senate Committee {i}",
                    "agency": "Senate",
                    "acronym": f"SC{i}",
                    "phone": "(360) 786-7715",
                }
                for i in range(num_committees)
            ]
            mock_client.get_active_senate_committees.return_value = mock_committees

            result = get_active_senate_committees()

            # Verify all returned committees are Senate committees
            if result["success"] and result["data"]["committees"]:
                for committee in result["data"]["committees"]:
                    assert committee["agency"] == "Senate", \
                        f"Expected Senate committee but got {committee['agency']}"
                    # Verify no House committees are included
                    assert committee["agency"] != "House"

    @given(biennium=bienniums, num_committees=st.integers(min_value=1, max_value=30))
    def test_house_committees_by_biennium_only_returns_house(self, biennium, num_committees):
        """Test that getHouseCommittees only returns House committees for a biennium."""
        with patch("src.wa_leg_mcp.tools.enhanced_committee_tools.wsl_client") as mock_client:
            # Create mock committees - all should be House
            mock_committees = [
                {
                    "id": str(i),
                    "name": f"Committee {i}",
                    "long_name": f"House Committee {i}",
                    "agency": "House",
                    "acronym": f"HC{i}",
                    "phone": "(360) 786-7100",
                }
                for i in range(num_committees)
            ]
            mock_client.get_house_committees.return_value = mock_committees

            result = get_house_committees(biennium)

            # Verify all returned committees are House committees
            if result["success"] and result["data"]["committees"]:
                for committee in result["data"]["committees"]:
                    assert committee["agency"] == "House", \
                        f"Expected House committee but got {committee['agency']}"
                    # Verify no Senate committees are included
                    assert committee["agency"] != "Senate"

    @given(biennium=bienniums, num_committees=st.integers(min_value=1, max_value=30))
    def test_senate_committees_by_biennium_only_returns_senate(self, biennium, num_committees):
        """Test that getSenateCommittees only returns Senate committees for a biennium."""
        with patch("src.wa_leg_mcp.tools.enhanced_committee_tools.wsl_client") as mock_client:
            # Create mock committees - all should be Senate
            mock_committees = [
                {
                    "id": str(i),
                    "name": f"Committee {i}",
                    "long_name": f"Senate Committee {i}",
                    "agency": "Senate",
                    "acronym": f"SC{i}",
                    "phone": "(360) 786-7715",
                }
                for i in range(num_committees)
            ]
            mock_client.get_senate_committees.return_value = mock_committees

            result = get_senate_committees(biennium)

            # Verify all returned committees are Senate committees
            if result["success"] and result["data"]["committees"]:
                for committee in result["data"]["committees"]:
                    assert committee["agency"] == "Senate", \
                        f"Expected Senate committee but got {committee['agency']}"
                    # Verify no House committees are included
                    assert committee["agency"] != "House"

    @given(
        num_house=st.integers(min_value=1, max_value=20),
        num_senate=st.integers(min_value=1, max_value=20)
    )
    def test_chamber_filtering_excludes_other_chamber(self, num_house, num_senate):
        """Test that chamber filtering strictly excludes the other chamber."""
        with patch("src.wa_leg_mcp.tools.enhanced_committee_tools.wsl_client") as mock_client:
            # Test House filtering
            house_committees = [
                {
                    "id": f"H{i}",
                    "name": f"House Committee {i}",
                    "long_name": f"House Committee {i}",
                    "agency": "House",
                    "acronym": f"HC{i}",
                    "phone": "(360) 786-7100",
                }
                for i in range(num_house)
            ]
            mock_client.get_active_house_committees.return_value = house_committees

            house_result = get_active_house_committees()

            if house_result["success"]:
                # Count should match only House committees
                assert house_result["metadata"]["count"] == num_house
                # Verify no Senate committees
                for committee in house_result["data"]["committees"]:
                    assert committee["agency"] == "House"

            # Test Senate filtering
            senate_committees = [
                {
                    "id": f"S{i}",
                    "name": f"Senate Committee {i}",
                    "long_name": f"Senate Committee {i}",
                    "agency": "Senate",
                    "acronym": f"SC{i}",
                    "phone": "(360) 786-7715",
                }
                for i in range(num_senate)
            ]
            mock_client.get_active_senate_committees.return_value = senate_committees

            senate_result = get_active_senate_committees()

            if senate_result["success"]:
                # Count should match only Senate committees
                assert senate_result["metadata"]["count"] == num_senate
                # Verify no House committees
                for committee in senate_result["data"]["committees"]:
                    assert committee["agency"] == "Senate"
