"""
Tests for rcw_tools.py
"""

from unittest.mock import patch

import pytest

from wa_leg_mcp.tools.rcw_tools import get_rcw_cites_affected


class TestGetRcwCitesAffected:
    """Tests for the get_rcw_cites_affected function."""

    def test_get_rcw_cites_success(self, common_test_data):
        """Test successful retrieval of RCW citations."""
        mock_rcw_data = [
            {
                "rcw_chapter": "28A.150",
                "rcw_section": "260",
                "action": "Amended",
            },
            {
                "rcw_chapter": "28A.150",
                "rcw_section": "270",
                "action": "Repealed",
            },
            {
                "rcw_chapter": "28A.150",
                "rcw_section": "280",
                "action": "Created",
            },
        ]

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_rcw_cites_affected.return_value = mock_rcw_data

            result = get_rcw_cites_affected("HB 1234")

            assert result["success"] is True
            assert "data" in result
            assert "rcw_citations" in result["data"]
            
            citations = result["data"]["rcw_citations"]
            assert len(citations["amended"]) == 1
            assert len(citations["repealed"]) == 1
            assert len(citations["created"]) == 1
            
            # Verify RCW notation formatting
            assert citations["amended"][0]["citation"] == "RCW 28A.150.260"
            assert citations["repealed"][0]["citation"] == "RCW 28A.150.270"
            assert citations["created"][0]["citation"] == "RCW 28A.150.280"

    def test_get_rcw_cites_empty_result(self, common_test_data):
        """Test handling of empty RCW citation results."""
        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_rcw_cites_affected.return_value = []

            result = get_rcw_cites_affected("HB 9999")

            assert result["success"] is True
            assert result["data"]["rcw_citations"]["amended"] == []
            assert result["data"]["rcw_citations"]["repealed"] == []
            assert result["data"]["rcw_citations"]["created"] == []
            assert result["data"]["total_count"] == 0
            assert "message" in result["metadata"]
            assert "No RCW citations found" in result["metadata"]["message"]

    def test_get_rcw_cites_with_explicit_biennium(self):
        """Test get_rcw_cites_affected with explicitly provided biennium."""
        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_client.get_rcw_cites_affected.return_value = []
            explicit_biennium = "2021-22"

            result = get_rcw_cites_affected("HB 1234", biennium=explicit_biennium)

            assert result["success"] is True
            assert result["data"]["biennium"] == explicit_biennium
            mock_client.get_rcw_cites_affected.assert_called_once_with(explicit_biennium, "HB 1234")

    def test_get_rcw_cites_requires_chamber_prefix(self):
        """Test that bill number without chamber prefix returns an error."""
        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"

            result = get_rcw_cites_affected("1234")

            assert result["success"] is False
            assert "error" in result
            assert "chamber prefix" in result["error"].lower()

    def test_get_rcw_cites_api_error(self, common_test_data):
        """Test that API errors are handled gracefully."""
        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_rcw_cites_affected.side_effect = Exception("API Error")

            result = get_rcw_cites_affected("HB 1234")

            assert result["success"] is False
            assert "error" in result
            assert "Failed to fetch RCW citations" in result["error"]

    def test_get_rcw_cites_organized_by_action_type(self, common_test_data):
        """Test that RCW citations are properly organized by action type."""
        mock_rcw_data = [
            {"rcw_chapter": "1", "rcw_section": "1", "action": "Amended"},
            {"rcw_chapter": "2", "rcw_section": "2", "action": "Repealed"},
            {"rcw_chapter": "3", "rcw_section": "3", "action": "New Section"},
            {"rcw_chapter": "4", "rcw_section": "4", "action": "Amended"},
            {"rcw_chapter": "5", "rcw_section": "5", "action": "Added"},
        ]

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_rcw_cites_affected.return_value = mock_rcw_data

            result = get_rcw_cites_affected("HB 1234")

            assert result["success"] is True
            citations = result["data"]["rcw_citations"]
            
            # Should have 2 amended, 1 repealed, 2 created
            assert len(citations["amended"]) == 2
            assert len(citations["repealed"]) == 1
            assert len(citations["created"]) == 2
            assert result["data"]["total_count"] == 5

    def test_get_rcw_cites_standard_notation_formatting(self, common_test_data):
        """Test that RCW citations are formatted in standard notation."""
        mock_rcw_data = [
            {
                "rcw_chapter": "28A.150",
                "rcw_section": "260",
                "action": "Amended",
            },
            {
                "rcw_chapter": "9.94A",
                "rcw_section": "030",
                "action": "Amended",
            },
        ]

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_rcw_cites_affected.return_value = mock_rcw_data

            result = get_rcw_cites_affected("HB 1234")

            assert result["success"] is True
            citations = result["data"]["rcw_citations"]["amended"]
            
            # Verify standard RCW notation (RCW Chapter.Section)
            assert citations[0]["citation"] == "RCW 28A.150.260"
            assert citations[1]["citation"] == "RCW 9.94A.030"

    def test_get_rcw_cites_none_return(self, common_test_data):
        """Test handling when API returns None."""
        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_rcw_cites_affected.return_value = None

            result = get_rcw_cites_affected("HB 1234")

            assert result["success"] is True
            assert result["data"]["total_count"] == 0
            assert "message" in result["metadata"]

    def test_get_rcw_cites_missing_fields(self, common_test_data):
        """Test handling of RCW citations with missing fields."""
        mock_rcw_data = [
            {
                "rcw_chapter": "28A.150",
                # Missing section
                "action": "Amended",
            },
            {
                # Missing chapter
                "rcw_section": "260",
                "action": "Amended",
            },
        ]

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_rcw_cites_affected.return_value = mock_rcw_data

            result = get_rcw_cites_affected("HB 1234")

            assert result["success"] is True
            citations = result["data"]["rcw_citations"]["amended"]
            
            # Should handle missing fields gracefully
            assert len(citations) == 2
            assert "RCW" in citations[0]["citation"]
            assert "RCW" in citations[1]["citation"]
