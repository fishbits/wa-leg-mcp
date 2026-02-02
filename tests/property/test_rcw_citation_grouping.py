"""
Property-based tests for RCW citation grouping.

Feature: missing-api-coverage
Property 7: RCW Citation Grouping

For any bill with RCW citations, the citations SHALL be organized by action type
(amended, repealed, created). Each citation SHALL appear in exactly one group,
and the total count SHALL equal the sum of citations across all groups.

Validates: Requirements 4.3
"""

from unittest.mock import patch

import pytest
from hypothesis import given, settings, strategies as st

from wa_leg_mcp.tools.rcw_tools import get_rcw_cites_affected


# Strategy for generating valid bienniums
biennium_strategy = st.sampled_from([
    "2021-22",
    "2023-24",
    "2025-26",
])

# Strategy for generating valid bill IDs (with chamber prefix)
bill_id_strategy = st.builds(
    lambda prefix, num: f"{prefix} {num}",
    st.sampled_from(["HB", "SB"]),
    st.integers(min_value=1000, max_value=9999)
)

# Strategy for generating RCW action types
action_strategy = st.sampled_from([
    "Amended",
    "Repealed",
    "Created",
    "New Section",
    "Added",
    "Amending",
    "Repealing",
])


def generate_mock_rcw_citation(chapter: str, section: str, action: str) -> dict:
    """Generate a mock RCW citation for testing."""
    return {
        "rcw_chapter": chapter,
        "rcw_section": section,
        "action": action,
    }


class TestRcwCitationGrouping:
    """Property tests for RCW citation grouping by action type."""

    @given(
        biennium=biennium_strategy,
        bill_id=bill_id_strategy,
        num_citations=st.integers(min_value=1, max_value=10)
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_citation_grouping_completeness(self, biennium, bill_id, num_citations):
        """
        Feature: missing-api-coverage, Property 7: RCW Citation Grouping
        
        Test that all citations are grouped and total count matches.
        """
        # Generate mock citations with various action types
        mock_citations = []
        for i in range(num_citations):
            action = ["Amended", "Repealed", "Created"][i % 3]
            mock_citations.append(
                generate_mock_rcw_citation(f"28A.{i}", f"{100+i}", action)
            )

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_rcw_cites_affected.return_value = mock_citations

            result = get_rcw_cites_affected(bill_id, biennium)

            # Property 7: RCW Citation Grouping
            assert result["success"] is True, "Result should be successful"
            
            citations = result["data"]["rcw_citations"]
            
            # Verify all groups exist
            assert "amended" in citations, "Must have 'amended' group"
            assert "repealed" in citations, "Must have 'repealed' group"
            assert "created" in citations, "Must have 'created' group"
            
            # Count citations in each group
            amended_count = len(citations["amended"])
            repealed_count = len(citations["repealed"])
            created_count = len(citations["created"])
            
            # Total count should match sum of all groups
            total_in_groups = amended_count + repealed_count + created_count
            assert result["data"]["total_count"] == total_in_groups, (
                f"Total count ({result['data']['total_count']}) must equal "
                f"sum of groups ({total_in_groups})"
            )
            
            # Total should match input
            assert total_in_groups == num_citations, (
                f"All {num_citations} citations must be grouped, got {total_in_groups}"
            )

    @given(
        biennium=biennium_strategy,
        bill_id=bill_id_strategy,
        num_amended=st.integers(min_value=0, max_value=5),
        num_repealed=st.integers(min_value=0, max_value=5),
        num_created=st.integers(min_value=0, max_value=5)
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_citation_grouping_by_action_type(self, biennium, bill_id, num_amended, num_repealed, num_created):
        """
        Feature: missing-api-coverage, Property 7: RCW Citation Grouping
        
        Test that citations are correctly grouped by action type.
        """
        # Generate mock citations with specific action types
        mock_citations = []
        
        for i in range(num_amended):
            mock_citations.append(
                generate_mock_rcw_citation(f"1.{i}", f"{i}", "Amended")
            )
        
        for i in range(num_repealed):
            mock_citations.append(
                generate_mock_rcw_citation(f"2.{i}", f"{i}", "Repealed")
            )
        
        for i in range(num_created):
            mock_citations.append(
                generate_mock_rcw_citation(f"3.{i}", f"{i}", "Created")
            )

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_rcw_cites_affected.return_value = mock_citations

            result = get_rcw_cites_affected(bill_id, biennium)

            # Property 7: RCW Citation Grouping (by action type)
            assert result["success"] is True
            
            citations = result["data"]["rcw_citations"]
            
            # Verify correct grouping
            assert len(citations["amended"]) == num_amended, (
                f"Expected {num_amended} amended citations, got {len(citations['amended'])}"
            )
            assert len(citations["repealed"]) == num_repealed, (
                f"Expected {num_repealed} repealed citations, got {len(citations['repealed'])}"
            )
            assert len(citations["created"]) == num_created, (
                f"Expected {num_created} created citations, got {len(citations['created'])}"
            )

    @given(
        biennium=biennium_strategy,
        bill_id=bill_id_strategy,
        num_citations=st.integers(min_value=1, max_value=10)
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_citation_no_duplicates_across_groups(self, biennium, bill_id, num_citations):
        """
        Feature: missing-api-coverage, Property 7: RCW Citation Grouping
        
        Test that each citation appears in exactly one group (no duplicates).
        """
        # Generate mock citations with unique identifiers
        mock_citations = []
        for i in range(num_citations):
            action = ["Amended", "Repealed", "Created"][i % 3]
            mock_citations.append(
                generate_mock_rcw_citation(f"UNIQUE.{i}", f"{i}", action)
            )

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_rcw_cites_affected.return_value = mock_citations

            result = get_rcw_cites_affected(bill_id, biennium)

            # Property 7: RCW Citation Grouping (no duplicates)
            assert result["success"] is True
            
            citations = result["data"]["rcw_citations"]
            
            # Collect all citations from all groups
            all_citations = []
            all_citations.extend(citations["amended"])
            all_citations.extend(citations["repealed"])
            all_citations.extend(citations["created"])
            
            # Extract unique identifiers (chapter.section)
            citation_ids = [f"{c['chapter']}.{c['section']}" for c in all_citations]
            
            # Verify no duplicates
            assert len(citation_ids) == len(set(citation_ids)), (
                "Each citation should appear in exactly one group (no duplicates)"
            )
            
            # Verify all citations are accounted for
            assert len(citation_ids) == num_citations, (
                f"All {num_citations} citations must be present, got {len(citation_ids)}"
            )

    @given(
        biennium=biennium_strategy,
        bill_id=bill_id_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_citation_grouping_with_empty_result(self, biennium, bill_id):
        """
        Feature: missing-api-coverage, Property 7: RCW Citation Grouping
        
        Test that empty results have all groups present but empty.
        """
        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_rcw_cites_affected.return_value = []

            result = get_rcw_cites_affected(bill_id, biennium)

            # Property 7: RCW Citation Grouping (empty case)
            assert result["success"] is True
            
            citations = result["data"]["rcw_citations"]
            
            # All groups should exist but be empty
            assert citations["amended"] == [], "Amended group should be empty list"
            assert citations["repealed"] == [], "Repealed group should be empty list"
            assert citations["created"] == [], "Created group should be empty list"
            assert result["data"]["total_count"] == 0, "Total count should be 0"

    @given(
        biennium=biennium_strategy,
        bill_id=bill_id_strategy,
        num_citations=st.integers(min_value=1, max_value=10)
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_citation_grouping_with_variant_action_names(self, biennium, bill_id, num_citations):
        """
        Feature: missing-api-coverage, Property 7: RCW Citation Grouping
        
        Test that variant action names are correctly mapped to groups.
        For example, "Amending" should map to "amended", "New Section" to "created".
        """
        # Generate mock citations with variant action names
        variant_actions = [
            ("Amending", "amended"),
            ("Repealing", "repealed"),
            ("New Section", "created"),
            ("Added", "created"),
        ]
        
        mock_citations = []
        expected_groups = {"amended": 0, "repealed": 0, "created": 0}
        
        for i in range(num_citations):
            action_variant, expected_group = variant_actions[i % len(variant_actions)]
            mock_citations.append(
                generate_mock_rcw_citation(f"{i}.1", f"{i}", action_variant)
            )
            expected_groups[expected_group] += 1

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_rcw_cites_affected.return_value = mock_citations

            result = get_rcw_cites_affected(bill_id, biennium)

            # Property 7: RCW Citation Grouping (variant names)
            assert result["success"] is True
            
            citations = result["data"]["rcw_citations"]
            
            # Verify variant action names are correctly mapped
            assert len(citations["amended"]) == expected_groups["amended"]
            assert len(citations["repealed"]) == expected_groups["repealed"]
            assert len(citations["created"]) == expected_groups["created"]
            
            # Total should still match
            total = sum(expected_groups.values())
            assert result["data"]["total_count"] == total
