"""
Property-based tests for amendment year format flexibility.

Feature: missing-api-coverage
Property 8: Year Format Flexibility

For any tool that accepts a year parameter, the tool SHALL accept both 2-digit
(e.g., "23") and 4-digit (e.g., "2023") year formats and treat them equivalently.
The tool SHALL normalize the year format internally and produce consistent results
regardless of which format is provided.

Validates: Requirements 2.5
"""

from unittest.mock import patch

import pytest
from hypothesis import given, settings, strategies as st

from wa_leg_mcp.tools.amendment_tools import get_amendments_for_year


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

# Strategy for generating valid years (2000-2099)
year_4digit_strategy = st.integers(min_value=2000, max_value=2099).map(str)


class TestAmendmentYearFormatFlexibility:
    """Property tests for year format flexibility in amendment tools."""

    @given(
        bill_number=bill_number_strategy,
        year_4digit=year_4digit_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_year_format_equivalence(self, bill_number, year_4digit):
        """
        Feature: missing-api-coverage, Property 8: Year Format Flexibility
        
        Test that 2-digit and 4-digit year formats produce equivalent results.
        For any year, calling the tool with "23" should produce the same result
        as calling it with "2023".
        """
        # Convert 4-digit year to 2-digit
        year_2digit = year_4digit[2:]  # e.g., "2023" -> "23"
        
        mock_amendments = [
            {
                "name": f"{bill_number}-S AMH TEST H1234.1",
                "bill_id": f"HB {bill_number}",
                "bill_number": int(bill_number.split()[-1]) if " " in bill_number else int(bill_number),
                "sponsor_name": "Test Sponsor",
                "description": "Test Amendment",
                "floor_action": "ADOPTED",
                "floor_action_date": None,
            }
        ]

        with (
            patch("wa_leg_mcp.tools.amendment_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = f"{year_4digit}-{str(int(year_4digit) + 1)[2:]}"
            mock_client.get_amendments_for_year.return_value = mock_amendments

            # Call with 4-digit year
            result_4digit = get_amendments_for_year(bill_number, year_4digit)
            
            # Reset mock
            mock_client.get_amendments_for_year.reset_mock()
            mock_client.get_amendments_for_year.return_value = mock_amendments
            
            # Call with 2-digit year
            result_2digit = get_amendments_for_year(bill_number, year_2digit)

            # Property 8: Year Format Flexibility
            # Both formats should succeed
            assert result_4digit["success"] is True, "4-digit year format should succeed"
            assert result_2digit["success"] is True, "2-digit year format should succeed"
            
            # Both should normalize to the same 4-digit year
            assert result_4digit["data"]["year"] == year_4digit, f"4-digit format should preserve year as {year_4digit}"
            assert result_2digit["data"]["year"] == year_4digit, f"2-digit format should normalize to {year_4digit}"
            
            # Both should call the API with the same integer year
            expected_year_int = int(year_4digit)
            
            # Check that both calls used the same year integer
            calls_4digit = mock_client.get_amendments_for_year.call_args_list
            assert len(calls_4digit) >= 1, "Should have called API for 2-digit year"
            
            # The API should be called with the integer year
            actual_year_arg = calls_4digit[0][0][0]
            assert actual_year_arg == expected_year_int, (
                f"API should be called with year {expected_year_int}, got {actual_year_arg}"
            )

    @given(
        bill_number=bill_number_strategy,
        year_4digit=year_4digit_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_year_format_consistency_with_empty_results(self, bill_number, year_4digit):
        """
        Feature: missing-api-coverage, Property 8: Year Format Flexibility
        
        Test that year format flexibility works consistently even with empty results.
        """
        year_2digit = year_4digit[2:]

        with (
            patch("wa_leg_mcp.tools.amendment_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = f"{year_4digit}-{str(int(year_4digit) + 1)[2:]}"
            mock_client.get_amendments_for_year.return_value = []

            # Call with 4-digit year
            result_4digit = get_amendments_for_year(bill_number, year_4digit)
            
            # Reset mock
            mock_client.get_amendments_for_year.reset_mock()
            mock_client.get_amendments_for_year.return_value = []
            
            # Call with 2-digit year
            result_2digit = get_amendments_for_year(bill_number, year_2digit)

            # Property 8: Year Format Flexibility (with empty results)
            assert result_4digit["success"] is True
            assert result_2digit["success"] is True
            
            # Both should have empty amendments
            assert result_4digit["data"]["amendments"] == []
            assert result_2digit["data"]["amendments"] == []
            
            # Both should normalize to the same year
            assert result_4digit["data"]["year"] == year_4digit
            assert result_2digit["data"]["year"] == year_4digit
            
            # Both should have descriptive messages
            assert "message" in result_4digit["metadata"]
            assert "message" in result_2digit["metadata"]

    @given(bill_number=bill_number_strategy)
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_year_format_boundary_values(self, bill_number):
        """
        Feature: missing-api-coverage, Property 8: Year Format Flexibility
        
        Test year format flexibility at boundary values (00, 99).
        """
        test_cases = [
            ("00", "2000"),
            ("01", "2001"),
            ("99", "2099"),
            ("2000", "2000"),
            ("2099", "2099"),
        ]

        with (
            patch("wa_leg_mcp.tools.amendment_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"
            mock_client.get_amendments_for_year.return_value = []

            for input_year, expected_normalized in test_cases:
                result = get_amendments_for_year(bill_number, input_year)
                
                # Property 8: Year Format Flexibility (boundary values)
                assert result["success"] is True, f"Year {input_year} should be valid"
                assert result["data"]["year"] == expected_normalized, (
                    f"Year {input_year} should normalize to {expected_normalized}, "
                    f"got {result['data']['year']}"
                )

    @given(bill_number=bill_number_strategy)
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_invalid_year_formats_rejected(self, bill_number):
        """
        Feature: missing-api-coverage, Property 8: Year Format Flexibility
        
        Test that invalid year formats are properly rejected.
        Only 2-digit and 4-digit formats should be accepted.
        """
        invalid_years = [
            "1",      # 1 digit
            "202",    # 3 digits
            "20233",  # 5 digits
            "abcd",   # non-numeric
            "",       # empty
        ]

        with (
            patch("wa_leg_mcp.tools.amendment_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = "2023-24"

            for invalid_year in invalid_years:
                result = get_amendments_for_year(bill_number, invalid_year)
                
                # Property 8: Year Format Flexibility (invalid formats)
                assert result["success"] is False, f"Year {invalid_year} should be rejected"
                assert "error" in result, f"Year {invalid_year} should return an error"
                assert "year" in result["error"].lower() or "format" in result["error"].lower(), (
                    f"Error message should mention year or format for {invalid_year}"
                )

    @given(
        bill_number=bill_number_strategy,
        year_4digit=year_4digit_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_year_format_with_whitespace(self, bill_number, year_4digit):
        """
        Feature: missing-api-coverage, Property 8: Year Format Flexibility
        
        Test that year formats with leading/trailing whitespace are handled correctly.
        """
        year_2digit = year_4digit[2:]
        
        # Add whitespace
        year_4digit_ws = f"  {year_4digit}  "
        year_2digit_ws = f"  {year_2digit}  "

        with (
            patch("wa_leg_mcp.tools.amendment_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = f"{year_4digit}-{str(int(year_4digit) + 1)[2:]}"
            mock_client.get_amendments_for_year.return_value = []

            # Test 4-digit with whitespace
            result_4digit = get_amendments_for_year(bill_number, year_4digit_ws)
            
            # Test 2-digit with whitespace
            result_2digit = get_amendments_for_year(bill_number, year_2digit_ws)

            # Property 8: Year Format Flexibility (with whitespace)
            assert result_4digit["success"] is True, "4-digit year with whitespace should succeed"
            assert result_2digit["success"] is True, "2-digit year with whitespace should succeed"
            
            # Both should normalize to the same year (without whitespace)
            assert result_4digit["data"]["year"] == year_4digit
            assert result_2digit["data"]["year"] == year_4digit
