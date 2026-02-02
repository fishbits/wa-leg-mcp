"""
Property-based tests for committee action retrieval tools.

These tests validate correctness properties for committee action tools using
property-based testing with hypothesis.
"""

import pytest
from hypothesis import given, strategies as st
from unittest.mock import patch

from src.wa_leg_mcp.tools.committee_action_tools import (
    get_committee_executive_actions_by_bill,
    get_committee_referrals_by_bill,
    get_do_pass_by_committee,
    get_in_committee,
)


# Test data strategies
bienniums = st.sampled_from(["2021-22", "2023-24", "2025-26"])
bill_numbers = st.integers(min_value=1000, max_value=9999)
agencies = st.sampled_from(["House", "Senate"])
committee_names = st.sampled_from(["Finance", "Ways & Means", "Education", "Transportation"])


@pytest.mark.property_test
class TestCommitteeActionRetrievalProperties:
    """
    Property 23: Committee Action Retrieval
    
    For any bill, calling getCommitteeExecutiveActionsByBill and getCommitteeReferralsByBill
    SHALL return all executive actions and referrals for that bill.
    
    **Validates: Requirements 7.1**
    """

    @given(biennium=bienniums, bill_number=bill_numbers)
    def test_committee_executive_actions_structure(self, biennium, bill_number):
        """Test that executive actions retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.committee_action_tools.wsl_client") as mock_client:
            mock_client.get_committee_executive_actions_by_bill.return_value = [
                {"committee_name": "Finance", "action": "Do Pass"}
            ]

            result = get_committee_executive_actions_by_bill(str(bill_number), biennium)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "executive_actions" in result["data"]
                assert isinstance(result["data"]["executive_actions"], list)

    @given(biennium=bienniums, bill_number=bill_numbers)
    def test_committee_referrals_structure(self, biennium, bill_number):
        """Test that referrals retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.committee_action_tools.wsl_client") as mock_client:
            mock_client.get_committee_referrals_by_bill.return_value = [
                {"committee_name": "Finance"}
            ]

            result = get_committee_referrals_by_bill(str(bill_number), biennium)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "referrals" in result["data"]
                assert isinstance(result["data"]["referrals"], list)


@pytest.mark.property_test
class TestBillsInCommitteeRetrievalProperties:
    """
    Property 24: Bills in Committee Retrieval
    
    For any committee and biennium, calling getInCommittee SHALL return all bills
    currently referred to that committee.
    
    **Validates: Requirements 7.2**
    """

    @given(biennium=bienniums, agency=agencies, committee_name=committee_names)
    def test_bills_in_committee_structure(self, biennium, agency, committee_name):
        """Test that bills in committee retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.committee_action_tools.wsl_client") as mock_client:
            mock_client.get_in_committee.return_value = [{"bill_id": "HB 1234"}]

            result = get_in_committee(committee_name, agency, biennium)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "bills_in_committee" in result["data"]
                assert isinstance(result["data"]["bills_in_committee"], list)

    @given(biennium=bienniums, agency=agencies, committee_name=committee_names)
    def test_bills_in_committee_empty_handling(self, biennium, agency, committee_name):
        """Test that committees with no bills return empty list with message."""
        with patch("src.wa_leg_mcp.tools.committee_action_tools.wsl_client") as mock_client:
            mock_client.get_in_committee.return_value = []

            result = get_in_committee(committee_name, agency, biennium)

            assert result["success"] is True
            assert result["data"]["bills_in_committee"] == []
            assert "message" in result["metadata"]


@pytest.mark.property_test
class TestDoPassFilteringProperties:
    """
    Property 25: Do Pass Filtering
    
    For any committee and biennium, calling getDoPassByCommittee SHALL return only bills
    that received a "do pass" recommendation from that committee.
    
    **Validates: Requirements 7.3**
    """

    @given(biennium=bienniums, agency=agencies, committee_name=committee_names)
    def test_do_pass_bills_structure(self, biennium, agency, committee_name):
        """Test that do pass bills retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.committee_action_tools.wsl_client") as mock_client:
            mock_client.get_do_pass_by_committee.return_value = [{"bill_id": "HB 5678"}]

            result = get_do_pass_by_committee(committee_name, agency, biennium)

            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "do_pass_bills" in result["data"]
                assert isinstance(result["data"]["do_pass_bills"], list)

    @given(biennium=bienniums, agency=agencies, committee_name=committee_names)
    def test_do_pass_bills_empty_handling(self, biennium, agency, committee_name):
        """Test that committees with no do pass bills return empty list with message."""
        with patch("src.wa_leg_mcp.tools.committee_action_tools.wsl_client") as mock_client:
            mock_client.get_do_pass_by_committee.return_value = []

            result = get_do_pass_by_committee(committee_name, agency, biennium)

            assert result["success"] is True
            assert result["data"]["do_pass_bills"] == []
            assert "message" in result["metadata"]

    @given(
        biennium=bienniums,
        agency=agencies,
        committee_name=committee_names,
        num_bills=st.integers(min_value=0, max_value=30)
    )
    def test_do_pass_bills_count_matches_list_length(self, biennium, agency, committee_name, num_bills):
        """Test that count metadata matches actual list length."""
        with patch("src.wa_leg_mcp.tools.committee_action_tools.wsl_client") as mock_client:
            mock_bills = [{"bill_id": f"HB {1000+i}"} for i in range(num_bills)]
            mock_client.get_do_pass_by_committee.return_value = mock_bills

            result = get_do_pass_by_committee(committee_name, agency, biennium)

            if result["success"]:
                assert result["metadata"]["count"] == len(result["data"]["do_pass_bills"])
                assert result["metadata"]["count"] == num_bills
