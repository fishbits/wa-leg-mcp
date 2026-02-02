"""
Property-based tests for amendment retrieval.

Feature: missing-api-coverage
Property 12: Amendment Retrieval by Biennium
Property 13: Amendment Retrieval by Year

For any valid bill and biennium/year combination, the amendment retrieval tools
SHALL return a consistent response structure with all required fields present.
When amendments exist, they SHALL include sponsor, status, and description fields.
When no amendments exist, the tool SHALL return an empty list with a descriptive message.

Validates: Requirements 2.1, 2.2
"""

from datetime import datetime
from unittest.mock import patch

import pytest
from hypothesis import given, settings, strategies as st

from wa_leg_mcp.tools.amendment_tools import (
    get_amendments_for_biennium,
    get_amendments_for_year,
)


# Strategy for generating valid bienniums
biennium_strategy = st.sampled_from([
    "2021-22",
    "2023-24",
    "2025-26",
])

# Strategy for generating valid years
year_strategy = st.integers(min_value=2020, max_value=2026).map(str)

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


def generate_mock_amendment(bill_num: int, index: int) -> dict:
    """Generate a mock amendment for testing."""
    return {
        "name": f"{bill_num}-S AMH SPONSOR{index} H{1000+index}.1",
        "bill_id": f"HB {bill_num}",
        "bill_number": bill_num,
        "legislative_session": "2023 Regular Session",
        "type": "Floor",
        "floor_number": 1000 + index,
        "sponsor_name": f"Sponsor{index}",
        "description": f"Amendment {index}",
        "drafter": f"H{1000+index}.1",
        "floor_action": "ADOPTED" if index % 2 == 0 else "WITHDRAWN",
        "floor_action_date": datetime(2023, 3, 15 + index),
        "document_exists": True,
        "htm_url": f"http://example.com/amendment{index}.htm",
        "pdf_url": f"http://example.com/amendment{index}.pdf",
        "agency": "House",
    }


class TestAmendmentRetrievalByBiennium:
    """Property tests for amendment retrieval by biennium."""

    @given(
        biennium=biennium_strategy,
        bill_number=bill_number_strategy,
        num_amendments=st.integers(min_value=1, max_value=5)
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_amendment_retrieval_structure_with_data(self, biennium, bill_number, num_amendments):
        """
        Feature: missing-api-coverage, Property 12: Amendment Retrieval by Biennium
        
        Test that amendment retrieval returns consistent structure with required fields.
        """
        # Extract bill number for mock data
        bill_num = int(bill_number.split()[-1]) if " " in bill_number else int(bill_number)
        
        # Generate mock amendments
        mock_amendments = [
            generate_mock_amendment(bill_num, i)
            for i in range(num_amendments)
        ]

        with (
            patch("wa_leg_mcp.tools.amendment_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_amendments_for_biennium.return_value = mock_amendments

            result = get_amendments_for_biennium(bill_number, biennium)

            # Property 12: Amendment Retrieval by Biennium
            # Verify top-level structure
            assert isinstance(result, dict), "Result must be a dictionary"
            assert "success" in result, "Result must have 'success' field"
            assert "data" in result, "Result must have 'data' field"
            assert "metadata" in result, "Result must have 'metadata' field"
            
            assert result["success"] is True, "Success field must be True"
            
            # Verify data structure
            data = result["data"]
            assert isinstance(data, dict), "Data must be a dictionary"
            assert "bill_number" in data, "Data must have 'bill_number' field"
            assert "biennium" in data, "Data must have 'biennium' field"
            assert "amendments" in data, "Data must have 'amendments' field"
            
            # Verify amendments list
            amendments = data["amendments"]
            assert isinstance(amendments, list), "Amendments must be a list"
            assert len(amendments) == num_amendments, f"Expected {num_amendments} amendments"
            
            # Verify each amendment has required fields
            for amendment in amendments:
                assert isinstance(amendment, dict), "Each amendment must be a dictionary"
                
                # Required fields per Requirement 2.3
                assert "name" in amendment, "Amendment must have 'name'"
                assert "sponsor_name" in amendment, "Amendment must have 'sponsor_name'"
                assert "description" in amendment, "Amendment must have 'description'"
                assert "floor_action" in amendment, "Amendment must have 'floor_action' (status)"
                
                # Additional fields
                assert "bill_id" in amendment
                assert "type" in amendment
                assert "htm_url" in amendment
                assert "pdf_url" in amendment

    @given(
        biennium=biennium_strategy,
        bill_number=bill_number_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_amendment_retrieval_empty_result(self, biennium, bill_number):
        """
        Feature: missing-api-coverage, Property 12: Amendment Retrieval by Biennium
        
        Test that empty results return consistent structure with descriptive message.
        """
        with (
            patch("wa_leg_mcp.tools.amendment_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_amendments_for_biennium.return_value = []

            result = get_amendments_for_biennium(bill_number, biennium)

            # Property 12: Amendment Retrieval by Biennium (empty case)
            assert result["success"] is True, "Empty results should still be successful"
            assert result["data"]["amendments"] == [], "Amendments should be empty list"
            assert "message" in result["metadata"], "Metadata should have descriptive message"
            assert "No amendments found" in result["metadata"]["message"]

    @given(
        biennium=biennium_strategy,
        bill_number=bill_number_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_amendment_retrieval_none_return(self, biennium, bill_number):
        """
        Feature: missing-api-coverage, Property 12: Amendment Retrieval by Biennium
        
        Test that None return from API is handled as empty result.
        """
        with (
            patch("wa_leg_mcp.tools.amendment_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_amendments_for_biennium.return_value = None

            result = get_amendments_for_biennium(bill_number, biennium)

            # Property 12: Amendment Retrieval by Biennium (None case)
            assert result["success"] is True
            assert result["data"]["amendments"] == []
            assert "message" in result["metadata"]


class TestAmendmentRetrievalByYear:
    """Property tests for amendment retrieval by year."""

    @given(
        year=year_strategy,
        bill_number=bill_number_strategy,
        num_amendments=st.integers(min_value=1, max_value=5)
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_amendment_retrieval_by_year_structure(self, year, bill_number, num_amendments):
        """
        Feature: missing-api-coverage, Property 13: Amendment Retrieval by Year
        
        Test that amendment retrieval by year returns consistent structure.
        """
        # Extract bill number for mock data
        bill_num = int(bill_number.split()[-1]) if " " in bill_number else int(bill_number)
        
        # Generate mock amendments
        mock_amendments = [
            generate_mock_amendment(bill_num, i)
            for i in range(num_amendments)
        ]

        with (
            patch("wa_leg_mcp.tools.amendment_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = f"{year}-{str(int(year) + 1)[2:]}"
            mock_client.get_amendments_for_year.return_value = mock_amendments

            result = get_amendments_for_year(bill_number, year)

            # Property 13: Amendment Retrieval by Year
            # Verify top-level structure
            assert isinstance(result, dict), "Result must be a dictionary"
            assert "success" in result, "Result must have 'success' field"
            assert "data" in result, "Result must have 'data' field"
            assert "metadata" in result, "Result must have 'metadata' field"
            
            assert result["success"] is True, "Success field must be True"
            
            # Verify data structure
            data = result["data"]
            assert isinstance(data, dict), "Data must be a dictionary"
            assert "bill_number" in data, "Data must have 'bill_number' field"
            assert "year" in data, "Data must have 'year' field"
            assert "amendments" in data, "Data must have 'amendments' field"
            
            # Verify amendments list
            amendments = data["amendments"]
            assert isinstance(amendments, list), "Amendments must be a list"
            assert len(amendments) == num_amendments, f"Expected {num_amendments} amendments"
            
            # Verify each amendment has required fields
            for amendment in amendments:
                assert isinstance(amendment, dict), "Each amendment must be a dictionary"
                
                # Required fields per Requirement 2.3
                assert "name" in amendment, "Amendment must have 'name'"
                assert "sponsor_name" in amendment, "Amendment must have 'sponsor_name'"
                assert "description" in amendment, "Amendment must have 'description'"
                assert "floor_action" in amendment, "Amendment must have 'floor_action' (status)"

    @given(
        year=year_strategy,
        bill_number=bill_number_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_amendment_retrieval_by_year_empty_result(self, year, bill_number):
        """
        Feature: missing-api-coverage, Property 13: Amendment Retrieval by Year
        
        Test that empty results return consistent structure with descriptive message.
        """
        with (
            patch("wa_leg_mcp.tools.amendment_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = f"{year}-{str(int(year) + 1)[2:]}"
            mock_client.get_amendments_for_year.return_value = []

            result = get_amendments_for_year(bill_number, year)

            # Property 13: Amendment Retrieval by Year (empty case)
            assert result["success"] is True, "Empty results should still be successful"
            assert result["data"]["amendments"] == [], "Amendments should be empty list"
            assert "message" in result["metadata"], "Metadata should have descriptive message"
            assert "No amendments found" in result["metadata"]["message"]

    @given(
        year=year_strategy,
        bill_number=bill_number_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_amendment_retrieval_by_year_none_return(self, year, bill_number):
        """
        Feature: missing-api-coverage, Property 13: Amendment Retrieval by Year
        
        Test that None return from API is handled as empty result.
        """
        with (
            patch("wa_leg_mcp.tools.amendment_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = f"{year}-{str(int(year) + 1)[2:]}"
            mock_client.get_amendments_for_year.return_value = None

            result = get_amendments_for_year(bill_number, year)

            # Property 13: Amendment Retrieval by Year (None case)
            assert result["success"] is True
            assert result["data"]["amendments"] == []
            assert "message" in result["metadata"]

    @given(
        year=year_strategy,
        bill_number=bill_number_strategy,
        num_amendments=st.integers(min_value=1, max_value=5)
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_amendment_fields_never_missing(self, year, bill_number, num_amendments):
        """
        Feature: missing-api-coverage, Property 13: Amendment Retrieval by Year
        
        Test that required amendment fields are always present, even if empty.
        """
        # Extract bill number for mock data
        bill_num = int(bill_number.split()[-1]) if " " in bill_number else int(bill_number)
        
        # Generate mock amendments with some missing fields
        mock_amendments = []
        for i in range(num_amendments):
            amendment = {
                "name": f"{bill_num}-S AMH SPONSOR{i} H{1000+i}.1",
                # Intentionally omit some fields to test handling
            }
            if i % 2 == 0:
                amendment["sponsor_name"] = f"Sponsor{i}"
            if i % 3 == 0:
                amendment["description"] = f"Description{i}"
            mock_amendments.append(amendment)

        with (
            patch("wa_leg_mcp.tools.amendment_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.amendment_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = f"{year}-{str(int(year) + 1)[2:]}"
            mock_client.get_amendments_for_year.return_value = mock_amendments

            result = get_amendments_for_year(bill_number, year)

            # Property 13: Amendment Retrieval by Year (missing fields)
            assert result["success"] is True
            
            # All amendments should have required fields, even if empty
            for amendment in result["data"]["amendments"]:
                assert "sponsor_name" in amendment, "sponsor_name must always be present"
                assert "description" in amendment, "description must always be present"
                assert "floor_action" in amendment, "floor_action must always be present"
                
                # Fields should be strings (empty string if missing from API)
                assert isinstance(amendment["sponsor_name"], str)
                assert isinstance(amendment["description"], str)
                assert isinstance(amendment["floor_action"], str)
