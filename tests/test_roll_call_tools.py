"""
Tests for roll_call_tools.py
"""

from unittest.mock import patch

import pytest

from wa_leg_mcp.tools.roll_call_tools import get_roll_calls


class TestGetRollCalls:
    """Tests for the get_roll_calls function."""

    @pytest.mark.parametrize(
        ("scenario", "mock_return", "expected_success", "expected_error"),
        [
            (
                "success_with_votes",
                [
                    {
                        "sequence_number": 1,
                        "vote_date": "2023-03-15",
                        "motion": "Final Passage",
                        "yea_count": 65,
                        "nay_count": 33,
                        "absent_count": 0,
                        "excused_count": 0,
                        "votes": {
                            "array_of_vote": [
                                {
                                    "name": "Smith, John",
                                    "vote_value": "Yea",
                                    "district": 1,
                                    "party": "D",
                                },
                                {
                                    "name": "Doe, Jane",
                                    "vote_value": "Nay",
                                    "district": 2,
                                    "party": "R",
                                },
                            ]
                        },
                    }
                ],
                True,
                None,
            ),
            (
                "empty_roll_calls",
                [],
                True,
                None,
            ),
            (
                "none_return",
                None,
                True,
                None,
            ),
        ],
    )
    def test_get_roll_calls_scenarios(
        self, scenario, mock_return, expected_success, expected_error, common_test_data
    ):
        """Test different scenarios for get_roll_calls using parametrization."""
        # Setup mocks
        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):

            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_roll_calls.return_value = mock_return

            # Call function
            result = get_roll_calls("HB 1234")

            # Assertions
            assert result["success"] == expected_success

            if expected_error:
                assert "error" in result
                assert expected_error in result["error"]
            else:
                assert "data" in result
                assert "metadata" in result

                # Check data structure
                data = result["data"]
                assert "bill_number" in data
                assert "biennium" in data
                assert "roll_calls" in data

                # If we have roll calls, verify structure
                if mock_return and len(mock_return) > 0:
                    assert len(data["roll_calls"]) > 0
                    roll_call = data["roll_calls"][0]
                    assert "sequence_number" in roll_call
                    assert "date" in roll_call
                    assert "description" in roll_call
                    assert "yea_votes" in roll_call
                    assert "nay_votes" in roll_call
                    assert "votes" in roll_call

                    # Verify votes structure
                    if len(roll_call["votes"]) > 0:
                        vote = roll_call["votes"][0]
                        assert "legislator_name" in vote
                        assert "vote" in vote
                        assert "district" in vote
                        assert "party" in vote

    def test_get_roll_calls_with_explicit_biennium(self, common_test_data):
        """Test get_roll_calls with explicitly provided biennium."""
        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):

            mock_client.get_roll_calls.return_value = []
            explicit_biennium = "2021-22"

            # Call function with explicit biennium
            result = get_roll_calls("HB 1234", biennium=explicit_biennium)

            # Verify the explicit biennium was used
            assert result["success"] is True
            assert result["data"]["biennium"] == explicit_biennium
            mock_client.get_roll_calls.assert_called_once_with(explicit_biennium, 1234)

    def test_get_roll_calls_bill_number_formats(self):
        """Test that various bill number formats are handled correctly."""
        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):

            mock_get_biennium.return_value = "2023-24"
            mock_client.get_roll_calls.return_value = []

            # Test different formats
            test_cases = [
                ("HB 1234", 1234),
                ("SB 5678", 5678),
                ("1234", 1234),
                ("5678", 5678),
            ]

            for bill_input, expected_num in test_cases:
                result = get_roll_calls(bill_input)
                assert result["success"] is True
                mock_client.get_roll_calls.assert_called_with("2023-24", expected_num)

    def test_get_roll_calls_invalid_bill_number(self):
        """Test that invalid bill numbers return an error."""
        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):

            mock_get_biennium.return_value = "2023-24"

            # Test invalid bill number
            result = get_roll_calls("INVALID")

            assert result["success"] is False
            assert "error" in result
            assert "Invalid bill number" in result["error"]

    def test_get_roll_calls_api_error(self, common_test_data):
        """Test that API errors are handled gracefully."""
        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):

            mock_get_biennium.return_value = common_test_data["biennium"]
            mock_client.get_roll_calls.side_effect = Exception("API Error")

            # Call function
            result = get_roll_calls("HB 1234")

            # Verify error handling
            assert result["success"] is False
            assert "error" in result
            assert "Failed to fetch roll calls" in result["error"]

    def test_get_roll_calls_chronological_ordering(self):
        """Test that roll calls are returned in chronological order."""
        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):

            mock_get_biennium.return_value = "2023-24"
            # Return roll calls out of order
            mock_client.get_roll_calls.return_value = [
                {
                    "sequence_number": 3,
                    "vote_date": "2023-03-20",
                    "motion": "Third Reading",
                    "yea_count": 70,
                    "nay_count": 28,
                    "absent_count": 0,
                    "excused_count": 0,
                    "votes": {"array_of_vote": []},
                },
                {
                    "sequence_number": 1,
                    "vote_date": "2023-03-15",
                    "motion": "First Reading",
                    "yea_count": 65,
                    "nay_count": 33,
                    "absent_count": 0,
                    "excused_count": 0,
                    "votes": {"array_of_vote": []},
                },
                {
                    "sequence_number": 2,
                    "vote_date": "2023-03-18",
                    "motion": "Second Reading",
                    "yea_count": 68,
                    "nay_count": 30,
                    "absent_count": 0,
                    "excused_count": 0,
                    "votes": {"array_of_vote": []},
                },
            ]

            result = get_roll_calls("HB 1234")

            # Verify chronological ordering
            assert result["success"] is True
            roll_calls = result["data"]["roll_calls"]
            assert len(roll_calls) == 3
            assert roll_calls[0]["sequence_number"] == 1
            assert roll_calls[1]["sequence_number"] == 2
            assert roll_calls[2]["sequence_number"] == 3

    def test_get_roll_calls_empty_result_message(self):
        """Test that empty results include a descriptive message."""
        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):

            mock_get_biennium.return_value = "2023-24"
            mock_client.get_roll_calls.return_value = []

            result = get_roll_calls("HB 9999")

            # Verify empty result handling
            assert result["success"] is True
            assert result["data"]["roll_calls"] == []
            assert "message" in result["metadata"]
            assert "No roll calls found" in result["metadata"]["message"]
