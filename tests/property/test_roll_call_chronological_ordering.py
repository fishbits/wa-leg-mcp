"""
Property-based tests for roll call chronological ordering.

Feature: missing-api-coverage
Property 4: Chronological Ordering

For any bill with multiple roll calls, the roll calls SHALL be returned in
chronological order based on sequence number and vote date. Earlier votes
SHALL appear before later votes in the returned list.

Validates: Requirements 1.3
"""

from datetime import datetime, timedelta
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


def generate_roll_call(sequence_number: int, base_date: datetime, motion: str) -> dict:
    """
    Generate a mock roll call with the given sequence number and date.
    
    Args:
        sequence_number: The sequence number for this roll call
        base_date: The base date for this roll call
        motion: The motion description
        
    Returns:
        A dictionary representing a roll call
    """
    vote_date = base_date + timedelta(days=sequence_number - 1)
    
    return {
        "sequence_number": sequence_number,
        "vote_date": vote_date.strftime("%Y-%m-%d"),
        "motion": motion,
        "yea_count": 50 + sequence_number,
        "nay_count": 40 - sequence_number,
        "absent_count": 5,
        "excused_count": 3,
        "votes": {
            "array_of_vote": [
                {
                    "name": f"Legislator {i}",
                    "vote_value": "Yea" if i % 2 == 0 else "Nay",
                    "district": i,
                    "party": "D" if i % 2 == 0 else "R",
                }
                for i in range(1, 6)
            ]
        },
    }


class TestRollCallChronologicalOrdering:
    """Property tests for roll call chronological ordering."""

    @given(
        biennium=biennium_strategy,
        bill_number=bill_number_strategy,
        num_roll_calls=st.integers(min_value=2, max_value=10)
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_chronological_ordering_by_sequence_number(self, biennium, bill_number, num_roll_calls):
        """
        Feature: missing-api-coverage, Property 4: Chronological Ordering
        
        Test that roll calls are returned in chronological order by sequence number.
        This test generates multiple roll calls with different sequence numbers
        in random order and verifies they are returned sorted.
        """
        base_date = datetime(2023, 1, 1)
        
        # Generate roll calls with sequence numbers
        sequence_numbers = list(range(1, num_roll_calls + 1))
        
        # Create roll calls in order
        mock_roll_calls = [
            generate_roll_call(seq, base_date, f"Motion {seq}")
            for seq in sequence_numbers
        ]
        
        # Shuffle the roll calls to simulate unordered API response
        import random
        shuffled_roll_calls = mock_roll_calls.copy()
        random.shuffle(shuffled_roll_calls)

        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_roll_calls.return_value = shuffled_roll_calls

            # Call the function
            response = get_roll_calls(bill_number, biennium=biennium)

            # Property 4: Chronological Ordering
            assert response["success"] is True, "Response should be successful"
            
            data = response["data"]
            roll_calls = data["roll_calls"]
            
            # Verify we got all roll calls
            assert len(roll_calls) == num_roll_calls, f"Expected {num_roll_calls} roll calls"
            
            # Verify chronological ordering by sequence number
            for i in range(len(roll_calls) - 1):
                current_seq = roll_calls[i]["sequence_number"]
                next_seq = roll_calls[i + 1]["sequence_number"]
                
                assert current_seq < next_seq, (
                    f"Roll calls must be in chronological order by sequence number. "
                    f"Found sequence {current_seq} before {next_seq} at positions {i} and {i+1}"
                )
            
            # Verify the sequence numbers are exactly what we expect
            actual_sequences = [rc["sequence_number"] for rc in roll_calls]
            expected_sequences = sorted(sequence_numbers)
            assert actual_sequences == expected_sequences, (
                f"Sequence numbers should be in order. "
                f"Expected {expected_sequences}, got {actual_sequences}"
            )

    @given(
        biennium=biennium_strategy,
        bill_number=bill_number_strategy,
        num_roll_calls=st.integers(min_value=2, max_value=10)
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_chronological_ordering_by_date(self, biennium, bill_number, num_roll_calls):
        """
        Feature: missing-api-coverage, Property 4: Chronological Ordering
        
        Test that roll calls with sequential dates are returned in chronological order.
        This test verifies that dates progress forward in time through the list.
        """
        base_date = datetime(2023, 1, 1)
        
        # Generate roll calls with sequential dates
        mock_roll_calls = [
            generate_roll_call(seq, base_date, f"Motion {seq}")
            for seq in range(1, num_roll_calls + 1)
        ]
        
        # Shuffle to simulate unordered API response
        import random
        shuffled_roll_calls = mock_roll_calls.copy()
        random.shuffle(shuffled_roll_calls)

        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_roll_calls.return_value = shuffled_roll_calls

            # Call the function
            response = get_roll_calls(bill_number, biennium=biennium)

            # Property 4: Chronological Ordering
            assert response["success"] is True, "Response should be successful"
            
            data = response["data"]
            roll_calls = data["roll_calls"]
            
            # Verify chronological ordering by date
            for i in range(len(roll_calls) - 1):
                current_date_str = roll_calls[i]["date"]
                next_date_str = roll_calls[i + 1]["date"]
                
                # Parse dates for comparison
                current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
                next_date = datetime.strptime(next_date_str, "%Y-%m-%d")
                
                assert current_date <= next_date, (
                    f"Roll calls must be in chronological order by date. "
                    f"Found date {current_date_str} before {next_date_str} at positions {i} and {i+1}"
                )

    @given(
        biennium=biennium_strategy,
        bill_number=bill_number_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_single_roll_call_ordering(self, biennium, bill_number):
        """
        Feature: missing-api-coverage, Property 4: Chronological Ordering
        
        Test that a single roll call is handled correctly (trivial ordering case).
        """
        base_date = datetime(2023, 1, 1)
        mock_roll_calls = [generate_roll_call(1, base_date, "Final Passage")]

        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_roll_calls.return_value = mock_roll_calls

            # Call the function
            response = get_roll_calls(bill_number, biennium=biennium)

            # Property 4: Chronological Ordering (trivial case)
            assert response["success"] is True, "Response should be successful"
            
            data = response["data"]
            roll_calls = data["roll_calls"]
            
            # Verify we got exactly one roll call
            assert len(roll_calls) == 1, "Expected exactly one roll call"
            assert roll_calls[0]["sequence_number"] == 1, "Sequence number should be 1"

    @given(
        biennium=biennium_strategy,
        bill_number=bill_number_strategy,
        num_roll_calls=st.integers(min_value=3, max_value=10)
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_reverse_ordered_input_becomes_chronological(self, biennium, bill_number, num_roll_calls):
        """
        Feature: missing-api-coverage, Property 4: Chronological Ordering
        
        Test that even when roll calls are provided in reverse chronological order,
        they are returned in forward chronological order.
        """
        base_date = datetime(2023, 1, 1)
        
        # Generate roll calls in forward order
        mock_roll_calls = [
            generate_roll_call(seq, base_date, f"Motion {seq}")
            for seq in range(1, num_roll_calls + 1)
        ]
        
        # Reverse them to simulate worst-case API response
        reversed_roll_calls = list(reversed(mock_roll_calls))

        with (
            patch("wa_leg_mcp.tools.roll_call_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.roll_call_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_roll_calls.return_value = reversed_roll_calls

            # Call the function
            response = get_roll_calls(bill_number, biennium=biennium)

            # Property 4: Chronological Ordering
            assert response["success"] is True, "Response should be successful"
            
            data = response["data"]
            roll_calls = data["roll_calls"]
            
            # Verify chronological ordering despite reverse input
            for i in range(len(roll_calls) - 1):
                current_seq = roll_calls[i]["sequence_number"]
                next_seq = roll_calls[i + 1]["sequence_number"]
                
                assert current_seq < next_seq, (
                    f"Roll calls must be in chronological order even when input is reversed. "
                    f"Found sequence {current_seq} before {next_seq}"
                )
            
            # Verify first and last are correct
            assert roll_calls[0]["sequence_number"] == 1, "First roll call should have sequence 1"
            assert roll_calls[-1]["sequence_number"] == num_roll_calls, (
                f"Last roll call should have sequence {num_roll_calls}"
            )
