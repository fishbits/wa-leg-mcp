"""
Property-based tests for roll call response structure.

Feature: missing-api-coverage
Property 1: Response Structure Consistency

For any MCP tool call that returns data successfully, the response SHALL have
the structure {"success": True, "data": Any, "metadata": dict} with all required
fields for that data type present (e.g., roll calls include legislator names and
votes, amendments include sponsor and status, committees include name and agency).

Validates: Requirements 1.2
"""

from unittest.mock import patch

import pytest
from hypothesis import given, settings, strategies as st

from wa_leg_mcp.tools.roll_call_tools import get_roll_calls


# Strategy for generating valid bienniums
biennium_strategy = st.sampled_from([
    "2021-22",
    "2023-24",
    "2025-26",
])

# Strategy for generating valid bill numbers
bill_number_strategy = st.one_of(
    # Format: "HB 1234" or "SB 5678"
    st.builds(
        lambda prefix, num: f"{prefix} {num}",
        st.sampled_from(["HB", "SB"]),
        st.integers(min_value=1000, max_value=9999)
    ),
    # Format: just the number "1234"
    st.integers(min_value=1000, max_value=9999).map(str)
)


class TestRollCallResponseStructure:
    """Property tests for roll call response structure consistency."""

    @given(
        biennium=biennium_strategy,
        bill_number=bill_number_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_response_structure_consistency_with_data(self, biennium, bill_number):
        """
        Feature: missing-api-coverage, Property 1: Response Structure Consistency
        
        Test that successful responses with data have consistent structure.
        This test mocks the API to return roll call data and verifies the response
        structure matches the specification.
        """
        # Mock data representing a successful API response with roll calls
        mock_roll_calls = [
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
        ]

        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_roll_calls.return_value = mock_roll_calls

            # Call the function
            response = get_roll_calls(bill_number, biennium=biennium)

            # Property 1: Response Structure Consistency
            # Verify top-level structure
            assert isinstance(response, dict), "Response must be a dictionary"
            assert "success" in response, "Response must have 'success' field"
            assert "data" in response, "Response must have 'data' field"
            assert "metadata" in response, "Response must have 'metadata' field"
            
            assert response["success"] is True, "Success field must be True for successful calls"
            
            # Verify data structure for roll calls
            data = response["data"]
            assert isinstance(data, dict), "Data must be a dictionary"
            assert "bill_number" in data, "Data must have 'bill_number' field"
            assert "biennium" in data, "Data must have 'biennium' field"
            assert "roll_calls" in data, "Data must have 'roll_calls' field"
            
            # Verify roll_calls is a list
            assert isinstance(data["roll_calls"], list), "roll_calls must be a list"
            
            # If roll calls exist, verify their structure
            if len(data["roll_calls"]) > 0:
                for roll_call in data["roll_calls"]:
                    assert isinstance(roll_call, dict), "Each roll call must be a dictionary"
                    
                    # Required fields for roll call
                    assert "sequence_number" in roll_call, "Roll call must have 'sequence_number'"
                    assert "date" in roll_call, "Roll call must have 'date'"
                    assert "description" in roll_call, "Roll call must have 'description'"
                    assert "yea_votes" in roll_call, "Roll call must have 'yea_votes'"
                    assert "nay_votes" in roll_call, "Roll call must have 'nay_votes'"
                    assert "absent_votes" in roll_call, "Roll call must have 'absent_votes'"
                    assert "excused_votes" in roll_call, "Roll call must have 'excused_votes'"
                    assert "votes" in roll_call, "Roll call must have 'votes'"
                    
                    # Verify votes structure
                    assert isinstance(roll_call["votes"], list), "votes must be a list"
                    
                    for vote in roll_call["votes"]:
                        assert isinstance(vote, dict), "Each vote must be a dictionary"
                        
                        # Required fields for individual votes
                        assert "legislator_name" in vote, "Vote must have 'legislator_name'"
                        assert "vote" in vote, "Vote must have 'vote' field"
                        assert "district" in vote, "Vote must have 'district'"
                        assert "party" in vote, "Vote must have 'party'"
            
            # Verify metadata structure
            metadata = response["metadata"]
            assert isinstance(metadata, dict), "Metadata must be a dictionary"
            assert "api_call" in metadata, "Metadata must have 'api_call' field"

    @given(
        biennium=biennium_strategy,
        bill_number=bill_number_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_response_structure_consistency_empty_data(self, biennium, bill_number):
        """
        Feature: missing-api-coverage, Property 1: Response Structure Consistency
        
        Test that successful responses with empty data have consistent structure.
        This test mocks the API to return no roll calls and verifies the response
        structure still matches the specification.
        """
        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_roll_calls.return_value = []

            # Call the function
            response = get_roll_calls(bill_number, biennium=biennium)

            # Property 1: Response Structure Consistency
            # Verify top-level structure (same as with data)
            assert isinstance(response, dict), "Response must be a dictionary"
            assert "success" in response, "Response must have 'success' field"
            assert "data" in response, "Response must have 'data' field"
            assert "metadata" in response, "Response must have 'metadata' field"
            
            assert response["success"] is True, "Success field must be True even with empty data"
            
            # Verify data structure for empty roll calls
            data = response["data"]
            assert isinstance(data, dict), "Data must be a dictionary"
            assert "bill_number" in data, "Data must have 'bill_number' field"
            assert "biennium" in data, "Data must have 'biennium' field"
            assert "roll_calls" in data, "Data must have 'roll_calls' field"
            
            # Verify roll_calls is an empty list
            assert isinstance(data["roll_calls"], list), "roll_calls must be a list"
            assert len(data["roll_calls"]) == 0, "roll_calls should be empty"
            
            # Verify metadata structure
            metadata = response["metadata"]
            assert isinstance(metadata, dict), "Metadata must be a dictionary"
            assert "message" in metadata, "Metadata must have 'message' for empty results"
            assert "api_call" in metadata, "Metadata must have 'api_call' field"

    @given(bill_number=bill_number_strategy)
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_response_structure_consistency_with_error(self, bill_number):
        """
        Feature: missing-api-coverage, Property 1: Response Structure Consistency
        
        Test that error responses have consistent structure.
        This test simulates an API error and verifies the error response structure.
        """
        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"
            mock_client.get_roll_calls.side_effect = Exception("API Error")

            # Call the function
            response = get_roll_calls(bill_number)

            # Property 3: Error Handling Consistency
            # Verify error response structure
            assert isinstance(response, dict), "Response must be a dictionary"
            assert "success" in response, "Response must have 'success' field"
            assert response["success"] is False, "Success field must be False for errors"
            assert "error" in response, "Error response must have 'error' field"
            assert isinstance(response["error"], str), "Error field must be a string"
            assert len(response["error"]) > 0, "Error message must not be empty"
            
            # Verify metadata structure for errors
            assert "metadata" in response, "Error response must have 'metadata' field"
            metadata = response["metadata"]
            assert isinstance(metadata, dict), "Metadata must be a dictionary"
            assert "tool_name" in metadata, "Metadata must have 'tool_name' field"
            assert "api_call" in metadata, "Metadata must have 'api_call' field"

    @given(
        biennium=biennium_strategy,
        bill_number=bill_number_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_response_structure_consistency_with_none_return(self, biennium, bill_number):
        """
        Feature: missing-api-coverage, Property 1: Response Structure Consistency
        
        Test that responses handle None return from API consistently.
        This test mocks the API to return None and verifies the response structure.
        """
        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_roll_calls.return_value = None

            # Call the function
            response = get_roll_calls(bill_number, biennium=biennium)

            # Property 1: Response Structure Consistency
            # Verify top-level structure
            assert isinstance(response, dict), "Response must be a dictionary"
            assert "success" in response, "Response must have 'success' field"
            assert "data" in response, "Response must have 'data' field"
            assert "metadata" in response, "Response must have 'metadata' field"
            
            assert response["success"] is True, "Success field must be True even with None return"
            
            # Verify data structure treats None as empty
            data = response["data"]
            assert isinstance(data, dict), "Data must be a dictionary"
            assert "roll_calls" in data, "Data must have 'roll_calls' field"
            assert isinstance(data["roll_calls"], list), "roll_calls must be a list"
            assert len(data["roll_calls"]) == 0, "roll_calls should be empty for None return"
