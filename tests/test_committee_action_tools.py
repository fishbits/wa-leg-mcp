"""
Unit tests for committee action tools.
"""

import pytest
from unittest.mock import patch

from src.wa_leg_mcp.tools.committee_action_tools import (
    get_committee_executive_actions_by_bill,
    get_committee_referrals_by_bill,
    get_committee_referrals_by_committee,
    get_do_pass_by_committee,
    get_in_committee,
    get_legislation_reported_out_of_committee,
)


@pytest.fixture
def mock_wsl_client():
    """Mock WSLClient for testing."""
    with patch("src.wa_leg_mcp.tools.committee_action_tools.wsl_client") as mock:
        yield mock


class TestGetCommitteeExecutiveActionsByBill:
    """Tests for get_committee_executive_actions_by_bill function."""

    def test_success(self, mock_wsl_client):
        """Test successful retrieval of executive actions."""
        mock_actions = [
            {"committee_name": "Finance", "action": "Do Pass", "action_date": "2023-02-15"}
        ]
        mock_wsl_client.get_committee_executive_actions_by_bill.return_value = mock_actions

        result = get_committee_executive_actions_by_bill("HB 1234", "2023-24")

        assert result["success"] is True
        assert len(result["data"]["executive_actions"]) == 1
        assert result["metadata"]["count"] == 1

    def test_empty(self, mock_wsl_client):
        """Test retrieval when no actions found."""
        mock_wsl_client.get_committee_executive_actions_by_bill.return_value = []

        result = get_committee_executive_actions_by_bill("HB 9999", "2023-24")

        assert result["success"] is True
        assert result["data"]["executive_actions"] == []
        assert "No committee executive actions" in result["metadata"]["message"]

    def test_invalid_bill_number(self, mock_wsl_client):
        """Test with invalid bill number."""
        result = get_committee_executive_actions_by_bill("INVALID", "2023-24")

        assert result["success"] is False
        assert "Invalid bill number format" in result["error"]


class TestGetCommitteeReferralsByBill:
    """Tests for get_committee_referrals_by_bill function."""

    def test_success(self, mock_wsl_client):
        """Test successful retrieval of referrals."""
        mock_referrals = [
            {"committee_name": "Ways & Means", "referral_date": "2023-01-20"}
        ]
        mock_wsl_client.get_committee_referrals_by_bill.return_value = mock_referrals

        result = get_committee_referrals_by_bill("SB 5678", "2023-24")

        assert result["success"] is True
        assert len(result["data"]["referrals"]) == 1
        assert result["metadata"]["count"] == 1

    def test_empty(self, mock_wsl_client):
        """Test retrieval when no referrals found."""
        mock_wsl_client.get_committee_referrals_by_bill.return_value = []

        result = get_committee_referrals_by_bill("HB 9999", "2023-24")

        assert result["success"] is True
        assert result["data"]["referrals"] == []

    def test_numeric_only(self, mock_wsl_client):
        """Test with numeric bill number."""
        mock_wsl_client.get_committee_referrals_by_bill.return_value = []

        result = get_committee_referrals_by_bill("1234", "2023-24")

        assert result["success"] is True
        mock_wsl_client.get_committee_referrals_by_bill.assert_called_once_with("2023-24", 1234)


class TestGetCommitteeReferralsByCommittee:
    """Tests for get_committee_referrals_by_committee function."""

    def test_success(self, mock_wsl_client):
        """Test successful retrieval of bills referred to committee."""
        mock_bills = [{"bill_id": "HB 1111"}, {"bill_id": "HB 2222"}]
        mock_wsl_client.get_committee_referrals_by_committee.return_value = mock_bills

        result = get_committee_referrals_by_committee("Finance", "House", "2023-24")

        assert result["success"] is True
        assert len(result["data"]["referred_bills"]) == 2
        assert result["metadata"]["count"] == 2

    def test_empty(self, mock_wsl_client):
        """Test retrieval when no bills referred."""
        mock_wsl_client.get_committee_referrals_by_committee.return_value = []

        result = get_committee_referrals_by_committee("Finance", "House", "2023-24")

        assert result["success"] is True
        assert result["data"]["referred_bills"] == []

    def test_invalid_agency(self, mock_wsl_client):
        """Test with invalid agency."""
        result = get_committee_referrals_by_committee("Finance", "Invalid", "2023-24")

        assert result["success"] is False
        assert "Invalid agency" in result["error"]

    def test_default_biennium(self, mock_wsl_client):
        """Test with default biennium."""
        mock_wsl_client.get_committee_referrals_by_committee.return_value = []

        with patch(
            "src.wa_leg_mcp.tools.committee_action_tools.get_current_biennium"
        ) as mock_biennium:
            mock_biennium.return_value = "2025-26"
            result = get_committee_referrals_by_committee("Finance", "House")

        assert result["success"] is True
        assert result["data"]["biennium"] == "2025-26"


class TestGetDoPassByCommittee:
    """Tests for get_do_pass_by_committee function."""

    def test_success(self, mock_wsl_client):
        """Test successful retrieval of do pass bills."""
        mock_bills = [{"bill_id": "HB 3333"}, {"bill_id": "HB 4444"}]
        mock_wsl_client.get_do_pass_by_committee.return_value = mock_bills

        result = get_do_pass_by_committee("Ways & Means", "Senate", "2023-24")

        assert result["success"] is True
        assert len(result["data"]["do_pass_bills"]) == 2
        assert result["metadata"]["count"] == 2

    def test_empty(self, mock_wsl_client):
        """Test retrieval when no do pass bills found."""
        mock_wsl_client.get_do_pass_by_committee.return_value = []

        result = get_do_pass_by_committee("Finance", "House", "2023-24")

        assert result["success"] is True
        assert result["data"]["do_pass_bills"] == []

    def test_invalid_agency(self, mock_wsl_client):
        """Test with invalid agency."""
        result = get_do_pass_by_committee("Finance", "Invalid", "2023-24")

        assert result["success"] is False
        assert "Invalid agency" in result["error"]


class TestGetInCommittee:
    """Tests for get_in_committee function."""

    def test_success(self, mock_wsl_client):
        """Test successful retrieval of bills in committee."""
        mock_bills = [{"bill_id": "HB 5555"}]
        mock_wsl_client.get_in_committee.return_value = mock_bills

        result = get_in_committee("Education", "House", "2023-24")

        assert result["success"] is True
        assert len(result["data"]["bills_in_committee"]) == 1
        assert result["metadata"]["count"] == 1

    def test_empty(self, mock_wsl_client):
        """Test retrieval when no bills in committee."""
        mock_wsl_client.get_in_committee.return_value = []

        result = get_in_committee("Education", "House", "2023-24")

        assert result["success"] is True
        assert result["data"]["bills_in_committee"] == []

    def test_invalid_agency(self, mock_wsl_client):
        """Test with invalid agency."""
        result = get_in_committee("Education", "Invalid", "2023-24")

        assert result["success"] is False
        assert "Invalid agency" in result["error"]


class TestGetLegislationReportedOutOfCommittee:
    """Tests for get_legislation_reported_out_of_committee function."""

    def test_success(self, mock_wsl_client):
        """Test successful retrieval of reported bills."""
        mock_bills = [{"bill_id": "HB 6666"}, {"bill_id": "HB 7777"}]
        mock_wsl_client.get_legislation_reported_out_of_committee.return_value = mock_bills

        result = get_legislation_reported_out_of_committee(
            "Finance", "House", "2023-01-01", "2023-12-31"
        )

        assert result["success"] is True
        assert len(result["data"]["reported_bills"]) == 2
        assert result["metadata"]["count"] == 2

    def test_empty(self, mock_wsl_client):
        """Test retrieval when no bills reported out."""
        mock_wsl_client.get_legislation_reported_out_of_committee.return_value = []

        result = get_legislation_reported_out_of_committee(
            "Finance", "House", "2023-01-01", "2023-12-31"
        )

        assert result["success"] is True
        assert result["data"]["reported_bills"] == []

    def test_invalid_agency(self, mock_wsl_client):
        """Test with invalid agency."""
        result = get_legislation_reported_out_of_committee(
            "Finance", "Invalid", "2023-01-01", "2023-12-31"
        )

        assert result["success"] is False
        assert "Invalid agency" in result["error"]

    def test_api_error(self, mock_wsl_client):
        """Test with API error."""
        mock_wsl_client.get_legislation_reported_out_of_committee.side_effect = Exception(
            "API error"
        )

        result = get_legislation_reported_out_of_committee(
            "Finance", "House", "2023-01-01", "2023-12-31"
        )

        assert result["success"] is False
        assert "Failed to fetch" in result["error"]
