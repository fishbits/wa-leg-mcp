"""
Tests for amendment_tools.py
"""

from datetime import datetime
from unittest.mock import patch

import pytest

from wa_leg_mcp.tools.amendment_tools import (
    get_amendments_for_biennium,
    get_amendments_for_year,
)


class TestGetAmendmentsForBiennium:
    """Tests for the get_amendments_for_biennium function."""

    def test_get_amendments_success(self, common_test_data):
        """Test successful retrieval of amendments."""
        mock_amendments = [
            {
                "name": "1234-S AMH SMIT H2345.1",
                "bill_id": "HB 1234",
                "bill_number": 1234,
                "legislative_session": "2023 Regular Session",
                "type": "Floor",
                "floor_number": 1234,
                "sponsor_name": "Smith",
                "description": "Striker",
                "drafter": "H2345.1",
                "floor_action": "ADOPTED",
                "floor_action_date": datetime(2023, 3, 15),
                "document_exists": True,
                "htm_url": "http://example.com/amendment.htm",
                "pdf_url": "http://example.com/amendment.pdf",
                "agency": "House",
            }
        ]

        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_amendments_for_biennium.return_value = mock_amendments

            result = get_amendments_for_biennium("HB 1234")

            assert result["success"] is True
            assert "data" in result
            assert "amendments" in result["data"]
            assert len(result["data"]["amendments"]) == 1

            amendment = result["data"]["amendments"][0]
            assert amendment["name"] == "1234-S AMH SMIT H2345.1"
            assert amendment["sponsor_name"] == "Smith"
            assert amendment["description"] == "Striker"
            assert amendment["floor_action"] == "ADOPTED"

    def test_get_amendments_empty_result(self, common_test_data):
        """Test handling of empty amendment results."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_amendments_for_biennium.return_value = []

            result = get_amendments_for_biennium("HB 9999")

            assert result["success"] is True
            assert result["data"]["amendments"] == []
            assert "message" in result["metadata"]
            assert "No amendments found" in result["metadata"]["message"]

    def test_get_amendments_with_explicit_biennium(self):
        """Test get_amendments_for_biennium with explicitly provided biennium."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_client.get_amendments_for_biennium.return_value = []
            explicit_biennium = "2021-22"

            result = get_amendments_for_biennium("HB 1234", biennium=explicit_biennium)

            assert result["success"] is True
            assert result["data"]["biennium"] == explicit_biennium
            mock_client.get_amendments_for_biennium.assert_called_once_with(
                explicit_biennium, 1234
            )

    def test_get_amendments_bill_number_formats(self):
        """Test that various bill number formats are handled correctly."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"
            mock_client.get_amendments_for_biennium.return_value = []

            test_cases = [
                ("HB 1234", 1234),
                ("SB 5678", 5678),
                ("1234", 1234),
                ("5678", 5678),
            ]

            for bill_input, expected_num in test_cases:
                result = get_amendments_for_biennium(bill_input)
                assert result["success"] is True
                mock_client.get_amendments_for_biennium.assert_called_with("2023-24", expected_num)

    def test_get_amendments_invalid_bill_number(self):
        """Test that invalid bill numbers return an error."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"

            result = get_amendments_for_biennium("INVALID")

            assert result["success"] is False
            assert "error" in result
            assert "Invalid bill number" in result["error"]

    def test_get_amendments_api_error(self, common_test_data):
        """Test that API errors are handled gracefully."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_amendments_for_biennium.side_effect = Exception("API Error")

            result = get_amendments_for_biennium("HB 1234")

            assert result["success"] is False
            assert "error" in result
            assert "Failed to fetch amendments" in result["error"]

    def test_get_amendments_none_return(self, common_test_data):
        """Test handling when API returns None."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_amendments_for_biennium.return_value = None

            result = get_amendments_for_biennium("HB 1234")

            assert result["success"] is True
            assert result["data"]["amendments"] == []
            assert "message" in result["metadata"]

    def test_get_amendments_missing_fields(self, common_test_data):
        """Test handling of amendments with missing fields."""
        mock_amendments = [
            {
                "name": "1234-S AMH SMIT H2345.1",
                # Missing most fields
            }
        ]

        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_amendments_for_biennium.return_value = mock_amendments

            result = get_amendments_for_biennium("HB 1234")

            assert result["success"] is True
            amendment = result["data"]["amendments"][0]
            assert amendment["name"] == "1234-S AMH SMIT H2345.1"
            assert amendment["sponsor_name"] == ""
            assert amendment["description"] == ""
            assert amendment["floor_action"] == ""

    def test_get_amendments_empty_bill_number(self):
        """Test that empty bill number returns validation error."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"

            result = get_amendments_for_biennium("")

            assert result["success"] is False
            assert "error" in result
            assert "Invalid bill number" in result["error"]

    def test_get_amendments_whitespace_bill_number(self):
        """Test that whitespace-only bill number returns validation error."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"

            result = get_amendments_for_biennium("   ")

            assert result["success"] is False
            assert "error" in result
            assert "Invalid bill number" in result["error"]

    def test_get_amendments_multiple_amendments(self, common_test_data):
        """Test handling of multiple amendments."""
        mock_amendments = [
            {
                "name": "1234-S AMH SMIT H2345.1",
                "bill_id": "HB 1234",
                "sponsor_name": "Smith",
                "description": "Striker",
                "floor_action": "ADOPTED",
                "floor_action_date": datetime(2023, 3, 15),
            },
            {
                "name": "1234-S AMH JONES H2346.1",
                "bill_id": "HB 1234",
                "sponsor_name": "Jones",
                "description": "Technical",
                "floor_action": "WITHDRAWN",
                "floor_action_date": datetime(2023, 3, 16),
            },
        ]

        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_amendments_for_biennium.return_value = mock_amendments

            result = get_amendments_for_biennium("HB 1234")

            assert result["success"] is True
            assert len(result["data"]["amendments"]) == 2
            assert result["metadata"]["count"] == 2
            assert result["data"]["amendments"][0]["sponsor_name"] == "Smith"
            assert result["data"]["amendments"][1]["sponsor_name"] == "Jones"



class TestGetAmendmentsForYear:
    """Tests for the get_amendments_for_year function."""

    def test_get_amendments_for_year_success(self):
        """Test successful retrieval of amendments by year."""
        mock_amendments = [
            {
                "name": "1234-S AMH SMIT H2345.1",
                "bill_id": "HB 1234",
                "bill_number": 1234,
                "sponsor_name": "Smith",
                "description": "Striker",
                "floor_action": "ADOPTED",
                "floor_action_date": datetime(2023, 3, 15),
            }
        ]

        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"
            mock_client.get_amendments_for_year.return_value = mock_amendments

            result = get_amendments_for_year("HB 1234", "2023")

            assert result["success"] is True
            assert result["data"]["year"] == "2023"
            assert len(result["data"]["amendments"]) == 1
            mock_client.get_amendments_for_year.assert_called_once_with(2023, 1234)

    def test_get_amendments_for_year_two_digit_format(self):
        """Test that 2-digit year format is handled correctly."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"
            mock_client.get_amendments_for_year.return_value = []

            # Test 2-digit year
            result = get_amendments_for_year("HB 1234", "23")

            assert result["success"] is True
            assert result["data"]["year"] == "2023"
            mock_client.get_amendments_for_year.assert_called_once_with(2023, 1234)

    def test_get_amendments_for_year_four_digit_format(self):
        """Test that 4-digit year format is handled correctly."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"
            mock_client.get_amendments_for_year.return_value = []

            # Test 4-digit year
            result = get_amendments_for_year("HB 1234", "2023")

            assert result["success"] is True
            assert result["data"]["year"] == "2023"
            mock_client.get_amendments_for_year.assert_called_once_with(2023, 1234)

    def test_get_amendments_for_year_default_year(self):
        """Test that default year is used when none provided."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"
            mock_client.get_amendments_for_year.return_value = []

            result = get_amendments_for_year("HB 1234")

            assert result["success"] is True
            assert result["data"]["year"] == "2023"
            mock_client.get_amendments_for_year.assert_called_once_with(2023, 1234)

    def test_get_amendments_for_year_invalid_year_format(self):
        """Test that invalid year format returns error."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"

            # Test invalid year format (3 digits)
            result = get_amendments_for_year("HB 1234", "202")

            assert result["success"] is False
            assert "error" in result
            assert "Invalid year format" in result["error"]

    def test_get_amendments_for_year_empty_result(self):
        """Test handling of empty amendment results."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"
            mock_client.get_amendments_for_year.return_value = []

            result = get_amendments_for_year("HB 9999", "2023")

            assert result["success"] is True
            assert result["data"]["amendments"] == []
            assert "message" in result["metadata"]
            assert "No amendments found" in result["metadata"]["message"]

    def test_get_amendments_for_year_api_error(self):
        """Test that API errors are handled gracefully."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"
            mock_client.get_amendments_for_year.side_effect = Exception("API Error")

            result = get_amendments_for_year("HB 1234", "2023")

            assert result["success"] is False
            assert "error" in result
            assert "Failed to fetch amendments" in result["error"]

    def test_get_amendments_for_year_invalid_bill_number(self):
        """Test that invalid bill numbers return an error."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"

            result = get_amendments_for_year("INVALID", "2023")

            assert result["success"] is False
            assert "error" in result
            assert "Invalid bill number" in result["error"]

    def test_get_amendments_for_year_none_return(self):
        """Test handling when API returns None."""
        with (
            patch(
                "wa_leg_mcp.tools.amendment_tools.get_current_biennium"
            ) as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"
            mock_client.get_amendments_for_year.return_value = None

            result = get_amendments_for_year("HB 1234", "2023")

            assert result["success"] is True
            assert result["data"]["amendments"] == []
            assert "message" in result["metadata"]
