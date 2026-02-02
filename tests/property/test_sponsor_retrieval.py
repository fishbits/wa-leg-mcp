"""
Property-based tests for sponsor retrieval tools.

These tests validate correctness properties for sponsor tools using
property-based testing with hypothesis.
"""

import pytest
from hypothesis import given, strategies as st
from unittest.mock import patch

from src.wa_leg_mcp.tools.sponsor_tools import (
    get_house_sponsors,
    get_requesters,
    get_senate_sponsors,
    get_sponsors,
)


# Test data strategies
bienniums = st.sampled_from(["2021-22", "2023-24", "2025-26"])
parties = st.sampled_from(["D", "R", "I"])
districts = st.integers(min_value=1, max_value=49).map(str)


@pytest.mark.property_test
class TestSponsorRetrievalCompletenessProperties:
    """
    Property 29: Sponsor Retrieval Completeness
    
    For any biennium, calling getSponsors SHALL return sponsor information for both
    chambers including name, party, district, and contact information.
    
    **Validates: Requirements 9.1**
    """

    @given(
        biennium=bienniums,
        num_house=st.integers(min_value=0, max_value=50),
        num_senate=st.integers(min_value=0, max_value=25)
    )
    def test_sponsors_include_both_chambers(self, biennium, num_house, num_senate):
        """Test that getSponsors returns sponsors from both chambers."""
        with patch("src.wa_leg_mcp.tools.sponsor_tools.wsl_client") as mock_client:
            # Create mock sponsors from both chambers
            mock_sponsors = []
            
            # Add House sponsors
            for i in range(num_house):
                mock_sponsors.append({
                    "id": f"H{i}",
                    "name": f"House Member {i}",
                    "long_name": f"Representative {i}",
                    "party": "D" if i % 2 == 0 else "R",
                    "district": str((i % 49) + 1),
                    "agency": "House",
                    "phone": "(360) 786-7100",
                    "email": f"house{i}@leg.wa.gov",
                    "first_name": f"First{i}",
                    "last_name": f"Last{i}",
                })
            
            # Add Senate sponsors
            for i in range(num_senate):
                mock_sponsors.append({
                    "id": f"S{i}",
                    "name": f"Senate Member {i}",
                    "long_name": f"Senator {i}",
                    "party": "D" if i % 2 == 0 else "R",
                    "district": str((i % 49) + 1),
                    "agency": "Senate",
                    "phone": "(360) 786-7715",
                    "email": f"senate{i}@leg.wa.gov",
                    "first_name": f"First{i}",
                    "last_name": f"Last{i}",
                })
            
            mock_client.get_sponsors.return_value = mock_sponsors

            result = get_sponsors(biennium)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"] and result["data"]["sponsors"]:
                # Verify we have sponsors from both chambers (if any exist)
                agencies = {sponsor["agency"] for sponsor in result["data"]["sponsors"]}
                
                if num_house > 0:
                    assert "House" in agencies
                if num_senate > 0:
                    assert "Senate" in agencies
                
                # Verify total count
                assert result["metadata"]["count"] == num_house + num_senate

    @given(biennium=bienniums, num_sponsors=st.integers(min_value=1, max_value=30))
    def test_sponsors_include_required_fields(self, biennium, num_sponsors):
        """Test that sponsors include all required fields."""
        with patch("src.wa_leg_mcp.tools.sponsor_tools.wsl_client") as mock_client:
            mock_sponsors = [
                {
                    "id": str(i),
                    "name": f"Member {i}",
                    "long_name": f"Representative {i}",
                    "party": "D" if i % 2 == 0 else "R",
                    "district": str((i % 49) + 1),
                    "agency": "House",
                    "phone": "(360) 786-7100",
                    "email": f"member{i}@leg.wa.gov",
                    "first_name": f"First{i}",
                    "last_name": f"Last{i}",
                }
                for i in range(num_sponsors)
            ]
            mock_client.get_sponsors.return_value = mock_sponsors

            result = get_sponsors(biennium)

            if result["success"] and result["data"]["sponsors"]:
                for sponsor in result["data"]["sponsors"]:
                    # Verify all required fields are present
                    assert "id" in sponsor
                    assert "name" in sponsor
                    assert "party" in sponsor
                    assert "district" in sponsor
                    assert "agency" in sponsor
                    assert "phone" in sponsor
                    assert "email" in sponsor

    @given(biennium=bienniums)
    def test_sponsors_empty_handling(self, biennium):
        """Test that empty sponsors return empty list with message."""
        with patch("src.wa_leg_mcp.tools.sponsor_tools.wsl_client") as mock_client:
            mock_client.get_sponsors.return_value = []

            result = get_sponsors(biennium)

            assert result["success"] is True
            assert result["data"]["sponsors"] == []
            assert "message" in result["metadata"]


@pytest.mark.property_test
class TestRequesterInformationRetrievalProperties:
    """
    Property 30: Requester Information Retrieval
    
    For any biennium, calling getRequesters SHALL return all entities authorized
    to request legislation.
    
    **Validates: Requirements 9.3**
    """

    @given(biennium=bienniums, num_requesters=st.integers(min_value=0, max_value=50))
    def test_requesters_structure(self, biennium, num_requesters):
        """Test that requesters retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.sponsor_tools.wsl_client") as mock_client:
            mock_requesters = [
                {
                    "id": str(i),
                    "name": f"Agency {i}",
                    "type": "Agency" if i % 2 == 0 else "Department",
                }
                for i in range(num_requesters)
            ]
            mock_client.get_requesters.return_value = mock_requesters

            result = get_requesters(biennium)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "requesters" in result["data"]
                assert isinstance(result["data"]["requesters"], list)
                assert result["metadata"]["count"] == num_requesters

    @given(biennium=bienniums)
    def test_requesters_empty_handling(self, biennium):
        """Test that empty requesters return empty list with message."""
        with patch("src.wa_leg_mcp.tools.sponsor_tools.wsl_client") as mock_client:
            mock_client.get_requesters.return_value = []

            result = get_requesters(biennium)

            assert result["success"] is True
            assert result["data"]["requesters"] == []
            assert "message" in result["metadata"]

    @given(biennium=bienniums, num_requesters=st.integers(min_value=1, max_value=30))
    def test_requesters_include_required_fields(self, biennium, num_requesters):
        """Test that requesters include all required fields."""
        with patch("src.wa_leg_mcp.tools.sponsor_tools.wsl_client") as mock_client:
            mock_requesters = [
                {
                    "id": str(i),
                    "name": f"Agency {i}",
                    "type": "Agency",
                }
                for i in range(num_requesters)
            ]
            mock_client.get_requesters.return_value = mock_requesters

            result = get_requesters(biennium)

            if result["success"] and result["data"]["requesters"]:
                for requester in result["data"]["requesters"]:
                    # Verify all required fields are present
                    assert "id" in requester
                    assert "name" in requester
                    assert "type" in requester


@pytest.mark.property_test
class TestChamberSpecificSponsorRetrievalProperties:
    """
    Test chamber-specific sponsor retrieval (House and Senate).
    
    These tests validate that chamber-specific sponsor tools correctly filter
    by chamber and return only sponsors from the specified chamber.
    """

    @given(biennium=bienniums, num_sponsors=st.integers(min_value=1, max_value=50))
    def test_house_sponsors_only_returns_house(self, biennium, num_sponsors):
        """Test that getHouseSponsors only returns House sponsors."""
        with patch("src.wa_leg_mcp.tools.sponsor_tools.wsl_client") as mock_client:
            mock_sponsors = [
                {
                    "id": str(i),
                    "name": f"House Member {i}",
                    "long_name": f"Representative {i}",
                    "party": "D" if i % 2 == 0 else "R",
                    "district": str((i % 49) + 1),
                    "agency": "House",
                    "phone": "(360) 786-7100",
                    "email": f"house{i}@leg.wa.gov",
                    "first_name": f"First{i}",
                    "last_name": f"Last{i}",
                }
                for i in range(num_sponsors)
            ]
            mock_client.get_house_sponsors.return_value = mock_sponsors

            result = get_house_sponsors(biennium)

            if result["success"] and result["data"]["sponsors"]:
                # All sponsors should be from House
                for sponsor in result["data"]["sponsors"]:
                    assert sponsor["agency"] == "House"
                    assert sponsor["agency"] != "Senate"

    @given(biennium=bienniums, num_sponsors=st.integers(min_value=1, max_value=25))
    def test_senate_sponsors_only_returns_senate(self, biennium, num_sponsors):
        """Test that getSenateSponsors only returns Senate sponsors."""
        with patch("src.wa_leg_mcp.tools.sponsor_tools.wsl_client") as mock_client:
            mock_sponsors = [
                {
                    "id": str(i),
                    "name": f"Senate Member {i}",
                    "long_name": f"Senator {i}",
                    "party": "D" if i % 2 == 0 else "R",
                    "district": str((i % 49) + 1),
                    "agency": "Senate",
                    "phone": "(360) 786-7715",
                    "email": f"senate{i}@leg.wa.gov",
                    "first_name": f"First{i}",
                    "last_name": f"Last{i}",
                }
                for i in range(num_sponsors)
            ]
            mock_client.get_senate_sponsors.return_value = mock_sponsors

            result = get_senate_sponsors(biennium)

            if result["success"] and result["data"]["sponsors"]:
                # All sponsors should be from Senate
                for sponsor in result["data"]["sponsors"]:
                    assert sponsor["agency"] == "Senate"
                    assert sponsor["agency"] != "House"
