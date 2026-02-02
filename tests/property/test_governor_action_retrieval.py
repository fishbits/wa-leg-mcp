"""
Property-based tests for governor action retrieval tools.

These tests validate correctness properties for governor action tools using
property-based testing with hypothesis.
"""

import pytest
from hypothesis import given, strategies as st
from unittest.mock import patch

from src.wa_leg_mcp.tools.governor_action_tools import (
    get_legislation_governor_signed,
    get_legislation_governor_veto,
    get_legislation_governor_partial_veto,
)


# Test data strategies
bienniums = st.sampled_from(["2021-22", "2023-24", "2025-26"])


@pytest.mark.property_test
class TestGovernorSignedBillsRetrievalProperties:
    """
    Property 20: Governor Signed Bills Retrieval
    
    For any biennium, calling getLegislationGovernorSigned SHALL return all bills
    signed by the governor during that biennium with action dates.
    
    **Validates: Requirements 6.1**
    """

    @given(biennium=bienniums)
    def test_governor_signed_bills_structure(self, biennium):
        """Test that governor signed bills retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.governor_action_tools.wsl_client") as mock_client:
            # Mock signed bills
            mock_client.get_legislation_governor_signed.side_effect = [
                [{"bill_id": "HB 1234", "bill_number": 1234}],
                [{"bill_id": "SB 5678", "bill_number": 5678}],
            ]

            result = get_legislation_governor_signed(biennium)

            # Verify response structure
            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "signed_bills" in result["data"]
                assert "count" in result["metadata"]
                assert isinstance(result["data"]["signed_bills"], list)

    @given(biennium=bienniums)
    def test_governor_signed_bills_empty_handling(self, biennium):
        """Test that bienniums with no signed bills return empty list with message."""
        with patch("src.wa_leg_mcp.tools.governor_action_tools.wsl_client") as mock_client:
            # Mock no signed bills
            mock_client.get_legislation_governor_signed.return_value = []

            result = get_legislation_governor_signed(biennium)

            # Verify response structure for empty results
            assert result["success"] is True
            assert result["data"]["signed_bills"] == []
            assert result["metadata"]["count"] == 0
            assert "message" in result["metadata"]

    @given(biennium=bienniums, num_house=st.integers(min_value=0, max_value=50), num_senate=st.integers(min_value=0, max_value=50))
    def test_governor_signed_bills_count_matches_list_length(self, biennium, num_house, num_senate):
        """Test that count metadata matches actual list length."""
        with patch("src.wa_leg_mcp.tools.governor_action_tools.wsl_client") as mock_client:
            # Mock varying number of signed bills
            mock_house_bills = [{"bill_id": f"HB {1000+i}", "bill_number": 1000+i} for i in range(num_house)]
            mock_senate_bills = [{"bill_id": f"SB {5000+i}", "bill_number": 5000+i} for i in range(num_senate)]
            
            mock_client.get_legislation_governor_signed.side_effect = [
                mock_house_bills,
                mock_senate_bills,
            ]

            result = get_legislation_governor_signed(biennium)

            if result["success"]:
                assert result["metadata"]["count"] == len(result["data"]["signed_bills"])
                assert result["metadata"]["count"] == num_house + num_senate

    @given(biennium=bienniums)
    def test_governor_signed_bills_includes_both_chambers(self, biennium):
        """Test that signed bills include both House and Senate bills."""
        with patch("src.wa_leg_mcp.tools.governor_action_tools.wsl_client") as mock_client:
            # Mock bills from both chambers
            mock_client.get_legislation_governor_signed.side_effect = [
                [{"bill_id": "HB 1111", "bill_number": 1111}],
                [{"bill_id": "SB 5555", "bill_number": 5555}],
            ]

            result = get_legislation_governor_signed(biennium)

            if result["success"] and len(result["data"]["signed_bills"]) > 0:
                # Verify both chambers are called
                assert mock_client.get_legislation_governor_signed.call_count == 2


@pytest.mark.property_test
class TestGovernorVetoedBillsRetrievalProperties:
    """
    Property 21: Governor Vetoed Bills Retrieval
    
    For any biennium, calling getLegislationGovernorVeto SHALL return all bills
    vetoed by the governor with veto messages included.
    
    **Validates: Requirements 6.2**
    """

    @given(biennium=bienniums)
    def test_governor_vetoed_bills_structure(self, biennium):
        """Test that governor vetoed bills retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.governor_action_tools.wsl_client") as mock_client:
            # Mock vetoed bills
            mock_client.get_legislation_governor_veto.side_effect = [
                [{"bill_id": "HB 2222", "bill_number": 2222, "veto_message": "Vetoed"}],
                [{"bill_id": "SB 6666", "bill_number": 6666, "veto_message": "Vetoed"}],
            ]

            result = get_legislation_governor_veto(biennium)

            # Verify response structure
            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "vetoed_bills" in result["data"]
                assert "count" in result["metadata"]
                assert isinstance(result["data"]["vetoed_bills"], list)

    @given(biennium=bienniums)
    def test_governor_vetoed_bills_empty_handling(self, biennium):
        """Test that bienniums with no vetoed bills return empty list with message."""
        with patch("src.wa_leg_mcp.tools.governor_action_tools.wsl_client") as mock_client:
            # Mock no vetoed bills
            mock_client.get_legislation_governor_veto.return_value = []

            result = get_legislation_governor_veto(biennium)

            # Verify response structure for empty results
            assert result["success"] is True
            assert result["data"]["vetoed_bills"] == []
            assert result["metadata"]["count"] == 0
            assert "message" in result["metadata"]

    @given(biennium=bienniums)
    def test_governor_vetoed_bills_includes_veto_message(self, biennium):
        """Test that vetoed bills include veto messages."""
        with patch("src.wa_leg_mcp.tools.governor_action_tools.wsl_client") as mock_client:
            # Mock vetoed bills with messages
            mock_client.get_legislation_governor_veto.side_effect = [
                [{"bill_id": "HB 3333", "veto_message": "This bill is vetoed because..."}],
                [],
            ]

            result = get_legislation_governor_veto(biennium)

            if result["success"] and len(result["data"]["vetoed_bills"]) > 0:
                # Verify veto message is present
                assert "veto_message" in result["data"]["vetoed_bills"][0]


@pytest.mark.property_test
class TestGovernorPartialVetoRetrievalProperties:
    """
    Property 22: Governor Partial Veto Retrieval
    
    For any biennium, calling getLegislationGovernorPartialVeto SHALL return all bills
    with line-item vetoes and the affected sections.
    
    **Validates: Requirements 6.3**
    """

    @given(biennium=bienniums)
    def test_governor_partial_veto_bills_structure(self, biennium):
        """Test that governor partial veto bills retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.governor_action_tools.wsl_client") as mock_client:
            # Mock partially vetoed bills
            mock_client.get_legislation_governor_partial_veto.side_effect = [
                [{"bill_id": "HB 4444", "bill_number": 4444, "partial_veto_message": "Sections 1-3"}],
                [{"bill_id": "SB 7777", "bill_number": 7777, "partial_veto_message": "Section 5"}],
            ]

            result = get_legislation_governor_partial_veto(biennium)

            # Verify response structure
            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "partial_veto_bills" in result["data"]
                assert "count" in result["metadata"]
                assert isinstance(result["data"]["partial_veto_bills"], list)

    @given(biennium=bienniums)
    def test_governor_partial_veto_bills_empty_handling(self, biennium):
        """Test that bienniums with no partial vetoes return empty list with message."""
        with patch("src.wa_leg_mcp.tools.governor_action_tools.wsl_client") as mock_client:
            # Mock no partial vetoes
            mock_client.get_legislation_governor_partial_veto.return_value = []

            result = get_legislation_governor_partial_veto(biennium)

            # Verify response structure for empty results
            assert result["success"] is True
            assert result["data"]["partial_veto_bills"] == []
            assert result["metadata"]["count"] == 0
            assert "message" in result["metadata"]

    @given(biennium=bienniums, num_house=st.integers(min_value=0, max_value=10), num_senate=st.integers(min_value=0, max_value=10))
    def test_governor_partial_veto_bills_count_matches_list_length(self, biennium, num_house, num_senate):
        """Test that count metadata matches actual list length."""
        with patch("src.wa_leg_mcp.tools.governor_action_tools.wsl_client") as mock_client:
            # Mock varying number of partial vetoes
            mock_house_bills = [{"bill_id": f"HB {2000+i}", "bill_number": 2000+i} for i in range(num_house)]
            mock_senate_bills = [{"bill_id": f"SB {6000+i}", "bill_number": 6000+i} for i in range(num_senate)]
            
            mock_client.get_legislation_governor_partial_veto.side_effect = [
                mock_house_bills,
                mock_senate_bills,
            ]

            result = get_legislation_governor_partial_veto(biennium)

            if result["success"]:
                assert result["metadata"]["count"] == len(result["data"]["partial_veto_bills"])
                assert result["metadata"]["count"] == num_house + num_senate
