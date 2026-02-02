"""
Unit tests for governor action tools.
"""

import pytest
from unittest.mock import MagicMock, patch

from src.wa_leg_mcp.tools.governor_action_tools import (
    get_legislation_governor_signed,
    get_legislation_governor_veto,
    get_legislation_governor_partial_veto,
)


@pytest.fixture
def mock_wsl_client():
    """Mock WSLClient for testing."""
    with patch("src.wa_leg_mcp.tools.governor_action_tools.wsl_client") as mock:
        yield mock


class TestGetLegislationGovernorSigned:
    """Tests for get_legislation_governor_signed function."""

    def test_get_legislation_governor_signed_success(self, mock_wsl_client):
        """Test successful retrieval of governor signed bills."""
        mock_house_bills = [
            {"bill_id": "HB 1234", "bill_number": 1234, "short_description": "Test bill 1"}
        ]
        mock_senate_bills = [
            {"bill_id": "SB 5678", "bill_number": 5678, "short_description": "Test bill 2"}
        ]
        mock_wsl_client.get_legislation_governor_signed.side_effect = [
            mock_house_bills,
            mock_senate_bills,
        ]

        result = get_legislation_governor_signed("2023-24")

        assert result["success"] is True
        assert result["data"]["biennium"] == "2023-24"
        assert len(result["data"]["signed_bills"]) == 2
        assert result["metadata"]["count"] == 2
        assert mock_wsl_client.get_legislation_governor_signed.call_count == 2

    def test_get_legislation_governor_signed_empty(self, mock_wsl_client):
        """Test retrieval when no signed bills found."""
        mock_wsl_client.get_legislation_governor_signed.return_value = []

        result = get_legislation_governor_signed("2023-24")

        assert result["success"] is True
        assert result["data"]["signed_bills"] == []
        assert result["metadata"]["count"] == 0
        assert "No bills signed" in result["metadata"]["message"]

    def test_get_legislation_governor_signed_default_biennium(self, mock_wsl_client):
        """Test retrieval with default biennium."""
        mock_wsl_client.get_legislation_governor_signed.return_value = []

        with patch(
            "src.wa_leg_mcp.tools.governor_action_tools.get_current_biennium"
        ) as mock_biennium:
            mock_biennium.return_value = "2025-26"
            result = get_legislation_governor_signed()

        assert result["success"] is True
        assert result["data"]["biennium"] == "2025-26"

    def test_get_legislation_governor_signed_api_error(self, mock_wsl_client):
        """Test retrieval with API error."""
        mock_wsl_client.get_legislation_governor_signed.side_effect = Exception(
            "API connection failed"
        )

        result = get_legislation_governor_signed("2023-24")

        assert result["success"] is False
        assert "Failed to fetch" in result["error"]
        assert result["error_type"] == "unexpected"

    def test_get_legislation_governor_signed_house_only(self, mock_wsl_client):
        """Test retrieval when only House bills are signed."""
        mock_house_bills = [{"bill_id": "HB 1111", "bill_number": 1111}]
        mock_wsl_client.get_legislation_governor_signed.side_effect = [mock_house_bills, None]

        result = get_legislation_governor_signed("2023-24")

        assert result["success"] is True
        assert len(result["data"]["signed_bills"]) == 1
        assert result["data"]["signed_bills"][0]["bill_id"] == "HB 1111"


class TestGetLegislationGovernorVeto:
    """Tests for get_legislation_governor_veto function."""

    def test_get_legislation_governor_veto_success(self, mock_wsl_client):
        """Test successful retrieval of governor vetoed bills."""
        mock_house_bills = [
            {
                "bill_id": "HB 2222",
                "bill_number": 2222,
                "veto_message": "Veto message 1",
            }
        ]
        mock_senate_bills = [
            {
                "bill_id": "SB 6666",
                "bill_number": 6666,
                "veto_message": "Veto message 2",
            }
        ]
        mock_wsl_client.get_legislation_governor_veto.side_effect = [
            mock_house_bills,
            mock_senate_bills,
        ]

        result = get_legislation_governor_veto("2023-24")

        assert result["success"] is True
        assert result["data"]["biennium"] == "2023-24"
        assert len(result["data"]["vetoed_bills"]) == 2
        assert result["metadata"]["count"] == 2

    def test_get_legislation_governor_veto_empty(self, mock_wsl_client):
        """Test retrieval when no vetoed bills found."""
        mock_wsl_client.get_legislation_governor_veto.return_value = []

        result = get_legislation_governor_veto("2023-24")

        assert result["success"] is True
        assert result["data"]["vetoed_bills"] == []
        assert result["metadata"]["count"] == 0
        assert "No bills vetoed" in result["metadata"]["message"]

    def test_get_legislation_governor_veto_default_biennium(self, mock_wsl_client):
        """Test retrieval with default biennium."""
        mock_wsl_client.get_legislation_governor_veto.return_value = []

        with patch(
            "src.wa_leg_mcp.tools.governor_action_tools.get_current_biennium"
        ) as mock_biennium:
            mock_biennium.return_value = "2025-26"
            result = get_legislation_governor_veto()

        assert result["success"] is True
        assert result["data"]["biennium"] == "2025-26"

    def test_get_legislation_governor_veto_api_error(self, mock_wsl_client):
        """Test retrieval with API error."""
        mock_wsl_client.get_legislation_governor_veto.side_effect = Exception(
            "API connection failed"
        )

        result = get_legislation_governor_veto("2023-24")

        assert result["success"] is False
        assert "Failed to fetch" in result["error"]

    def test_get_legislation_governor_veto_includes_veto_message(self, mock_wsl_client):
        """Test that veto message is included in response."""
        mock_bills = [
            {
                "bill_id": "HB 3333",
                "bill_number": 3333,
                "veto_message": "This bill is vetoed because...",
            }
        ]
        mock_wsl_client.get_legislation_governor_veto.side_effect = [mock_bills, []]

        result = get_legislation_governor_veto("2023-24")

        assert result["success"] is True
        assert "veto_message" in result["data"]["vetoed_bills"][0]


class TestGetLegislationGovernorPartialVeto:
    """Tests for get_legislation_governor_partial_veto function."""

    def test_get_legislation_governor_partial_veto_success(self, mock_wsl_client):
        """Test successful retrieval of governor partially vetoed bills."""
        mock_house_bills = [
            {
                "bill_id": "HB 4444",
                "bill_number": 4444,
                "partial_veto_message": "Sections 1-3 vetoed",
            }
        ]
        mock_senate_bills = [
            {
                "bill_id": "SB 7777",
                "bill_number": 7777,
                "partial_veto_message": "Section 5 vetoed",
            }
        ]
        mock_wsl_client.get_legislation_governor_partial_veto.side_effect = [
            mock_house_bills,
            mock_senate_bills,
        ]

        result = get_legislation_governor_partial_veto("2023-24")

        assert result["success"] is True
        assert result["data"]["biennium"] == "2023-24"
        assert len(result["data"]["partial_veto_bills"]) == 2
        assert result["metadata"]["count"] == 2

    def test_get_legislation_governor_partial_veto_empty(self, mock_wsl_client):
        """Test retrieval when no partially vetoed bills found."""
        mock_wsl_client.get_legislation_governor_partial_veto.return_value = []

        result = get_legislation_governor_partial_veto("2023-24")

        assert result["success"] is True
        assert result["data"]["partial_veto_bills"] == []
        assert result["metadata"]["count"] == 0
        assert "No bills partially vetoed" in result["metadata"]["message"]

    def test_get_legislation_governor_partial_veto_default_biennium(self, mock_wsl_client):
        """Test retrieval with default biennium."""
        mock_wsl_client.get_legislation_governor_partial_veto.return_value = []

        with patch(
            "src.wa_leg_mcp.tools.governor_action_tools.get_current_biennium"
        ) as mock_biennium:
            mock_biennium.return_value = "2025-26"
            result = get_legislation_governor_partial_veto()

        assert result["success"] is True
        assert result["data"]["biennium"] == "2025-26"

    def test_get_legislation_governor_partial_veto_api_error(self, mock_wsl_client):
        """Test retrieval with API error."""
        mock_wsl_client.get_legislation_governor_partial_veto.side_effect = Exception(
            "API connection failed"
        )

        result = get_legislation_governor_partial_veto("2023-24")

        assert result["success"] is False
        assert "Failed to fetch" in result["error"]

    def test_get_legislation_governor_partial_veto_senate_only(self, mock_wsl_client):
        """Test retrieval when only Senate bills are partially vetoed."""
        mock_senate_bills = [{"bill_id": "SB 8888", "bill_number": 8888}]
        mock_wsl_client.get_legislation_governor_partial_veto.side_effect = [
            None,
            mock_senate_bills,
        ]

        result = get_legislation_governor_partial_veto("2023-24")

        assert result["success"] is True
        assert len(result["data"]["partial_veto_bills"]) == 1
        assert result["data"]["partial_veto_bills"][0]["bill_id"] == "SB 8888"
