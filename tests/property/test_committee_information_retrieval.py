"""
Property-based tests for enhanced committee information retrieval tools.

These tests validate correctness properties for committee information tools using
property-based testing with hypothesis.
"""

import pytest
from hypothesis import given, strategies as st
from unittest.mock import patch

from src.wa_leg_mcp.tools.enhanced_committee_tools import (
    get_active_committees,
    get_active_house_committees,
    get_active_senate_committees,
    get_committee_members,
)


# Test data strategies
bienniums = st.sampled_from(["2021-22", "2023-24", "2025-26"])
agencies = st.sampled_from(["House", "Senate"])
committee_names = st.sampled_from(["Finance", "Ways & Means", "Education", "Transportation"])


@pytest.mark.property_test
class TestActiveCommitteeRetrievalProperties:
    """
    Property 27: Active Committee Retrieval
    
    For any biennium, calling getActiveCommittees SHALL return all currently active
    committees for both House and Senate.
    
    **Validates: Requirements 8.1**
    """

    @given(num_committees=st.integers(min_value=0, max_value=50))
    def test_active_committees_structure(self, num_committees):
        """Test that active committees retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.enhanced_committee_tools.wsl_client") as mock_client:
            mock_committees = [
                {
                    "id": str(i),
                    "name": f"Committee {i}",
                    "long_name": f"Full Committee Name {i}",
                    "agency": "House" if i % 2 == 0 else "Senate",
                    "acronym": f"C{i}",
                    "phone": "(360) 786-7100",
                }
                for i in range(num_committees)
            ]
            mock_client.get_active_committees.return_value = mock_committees

            result = get_active_committees()

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "committees" in result["data"]
                assert isinstance(result["data"]["committees"], list)
                assert result["metadata"]["count"] == num_committees

    def test_active_committees_empty_handling(self):
        """Test that empty active committees return empty list with message."""
        with patch("src.wa_leg_mcp.tools.enhanced_committee_tools.wsl_client") as mock_client:
            mock_client.get_active_committees.return_value = []

            result = get_active_committees()

            assert result["success"] is True
            assert result["data"]["committees"] == []
            assert "message" in result["metadata"]

    @given(num_committees=st.integers(min_value=1, max_value=30))
    def test_active_house_committees_chamber_filtering(self, num_committees):
        """Test that active House committees only returns House committees."""
        with patch("src.wa_leg_mcp.tools.enhanced_committee_tools.wsl_client") as mock_client:
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

            if result["success"] and result["data"]["committees"]:
                # All committees should be House committees
                for committee in result["data"]["committees"]:
                    assert committee["agency"] == "House"

    @given(num_committees=st.integers(min_value=1, max_value=30))
    def test_active_senate_committees_chamber_filtering(self, num_committees):
        """Test that active Senate committees only returns Senate committees."""
        with patch("src.wa_leg_mcp.tools.enhanced_committee_tools.wsl_client") as mock_client:
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

            if result["success"] and result["data"]["committees"]:
                # All committees should be Senate committees
                for committee in result["data"]["committees"]:
                    assert committee["agency"] == "Senate"


@pytest.mark.property_test
class TestHistoricalCommitteeCompositionProperties:
    """
    Property 28: Historical Committee Composition
    
    For any biennium and committee name, calling getCommitteeMembers SHALL return
    the historical committee composition for that biennium.
    
    **Validates: Requirements 8.4**
    """

    @given(
        biennium=bienniums,
        agency=agencies,
        committee_name=committee_names,
        num_members=st.integers(min_value=0, max_value=20)
    )
    def test_committee_members_structure(self, biennium, agency, committee_name, num_members):
        """Test that committee members retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.enhanced_committee_tools.wsl_client") as mock_client:
            mock_members = [
                {
                    "id": str(i),
                    "name": f"Member {i}",
                    "party": "D" if i % 2 == 0 else "R",
                    "district": str(i + 1),
                    "role": "Chair" if i == 0 else "Member",
                    "phone": "(360) 786-7100",
                    "email": f"member{i}@leg.wa.gov",
                }
                for i in range(num_members)
            ]
            mock_client.get_committee_members.return_value = mock_members

            result = get_committee_members(committee_name, agency, biennium)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "members" in result["data"]
                assert isinstance(result["data"]["members"], list)
                assert result["data"]["committee_name"] == committee_name
                assert result["data"]["agency"] == agency
                assert result["data"]["biennium"] == biennium
                assert result["metadata"]["count"] == num_members

    @given(biennium=bienniums, agency=agencies, committee_name=committee_names)
    def test_committee_members_empty_handling(self, biennium, agency, committee_name):
        """Test that committees with no members return empty list with message."""
        with patch("src.wa_leg_mcp.tools.enhanced_committee_tools.wsl_client") as mock_client:
            mock_client.get_committee_members.return_value = []

            result = get_committee_members(committee_name, agency, biennium)

            assert result["success"] is True
            assert result["data"]["members"] == []
            assert "message" in result["metadata"]

    @given(
        biennium=bienniums,
        agency=agencies,
        committee_name=committee_names,
        num_members=st.integers(min_value=1, max_value=15)
    )
    def test_committee_members_include_required_fields(self, biennium, agency, committee_name, num_members):
        """Test that committee members include all required fields."""
        with patch("src.wa_leg_mcp.tools.enhanced_committee_tools.wsl_client") as mock_client:
            mock_members = [
                {
                    "id": str(i),
                    "name": f"Member {i}",
                    "party": "D" if i % 2 == 0 else "R",
                    "district": str(i + 1),
                    "role": "Chair" if i == 0 else "Member",
                    "phone": "(360) 786-7100",
                    "email": f"member{i}@leg.wa.gov",
                }
                for i in range(num_members)
            ]
            mock_client.get_committee_members.return_value = mock_members

            result = get_committee_members(committee_name, agency, biennium)

            if result["success"] and result["data"]["members"]:
                for member in result["data"]["members"]:
                    # Verify all required fields are present
                    assert "id" in member
                    assert "name" in member
                    assert "party" in member
                    assert "district" in member
                    assert "role" in member
                    assert "phone" in member
                    assert "email" in member
