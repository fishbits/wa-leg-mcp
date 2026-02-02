"""
Property-based tests for RCW notation formatting.

Feature: missing-api-coverage
Property 10: RCW Notation Formatting

For any RCW citation with chapter and section numbers, the citation SHALL be
formatted in standard RCW notation: "RCW Chapter.Section" (e.g., "RCW 28A.150.260").
The formatting SHALL be consistent across all citations regardless of input format.

Validates: Requirements 4.5
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

# Strategy for generating RCW chapters (various formats)
rcw_chapter_strategy = st.one_of(
    # Simple chapters: "1", "2", "9"
    st.integers(min_value=1, max_value=99).map(str),
    # Decimal chapters: "28A.150", "9.94A"
    st.builds(
        lambda major, minor: f"{major}.{minor}",
        st.integers(min_value=1, max_value=99),
        st.sampled_from(["1", "10", "100", "150", "94A", "A"])
    ),
)

# Strategy for generating RCW sections
rcw_section_strategy = st.one_of(
    # Simple sections: "010", "260"
    st.integers(min_value=1, max_value=999).map(lambda x: f"{x:03d}"),
    # Without leading zeros: "1", "10", "260"
    st.integers(min_value=1, max_value=999).map(str),
)


def generate_mock_rcw_citation(chapter: str, section: str) -> dict:
    """Generate a mock RCW citation for testing."""
    return {
        "rcw_chapter": chapter,
        "rcw_section": section,
        "action": "Amended",
    }


class TestRcwNotationFormatting:
    """Property tests for RCW notation formatting."""

    @given(
        biennium=biennium_strategy,
        bill_id=bill_id_strategy,
        chapter=rcw_chapter_strategy,
        section=rcw_section_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_rcw_notation_format_structure(self, biennium, bill_id, chapter, section):
        """
        Feature: missing-api-coverage, Property 10: RCW Notation Formatting
        
        Test that RCW citations are formatted as "RCW Chapter.Section".
        """
        mock_citations = [generate_mock_rcw_citation(chapter, section)]

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_rcw_cites_affected.return_value = mock_citations

            result = get_rcw_cites_affected(bill_id, biennium)

            # Property 10: RCW Notation Formatting
            assert result["success"] is True
            
            citations = result["data"]["rcw_citations"]["amended"]
            assert len(citations) == 1
            
            citation = citations[0]
            formatted_citation = citation["citation"]
            
            # Must start with "RCW "
            assert formatted_citation.startswith("RCW "), (
                f"Citation must start with 'RCW ', got: {formatted_citation}"
            )
            
            # Must contain the chapter and section
            assert chapter in formatted_citation, (
                f"Citation must contain chapter '{chapter}', got: {formatted_citation}"
            )
            assert section in formatted_citation, (
                f"Citation must contain section '{section}', got: {formatted_citation}"
            )
            
            # Standard format: "RCW Chapter.Section"
            expected_format = f"RCW {chapter}.{section}"
            assert formatted_citation == expected_format, (
                f"Expected format '{expected_format}', got: {formatted_citation}"
            )

    @given(
        biennium=biennium_strategy,
        bill_id=bill_id_strategy,
        num_citations=st.integers(min_value=2, max_value=5)
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_rcw_notation_consistency_across_citations(self, biennium, bill_id, num_citations):
        """
        Feature: missing-api-coverage, Property 10: RCW Notation Formatting
        
        Test that formatting is consistent across multiple citations.
        """
        mock_citations = []
        for i in range(num_citations):
            chapter = f"{10 + i}.{100 + i}"
            section = f"{200 + i}"
            mock_citations.append(generate_mock_rcw_citation(chapter, section))

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_rcw_cites_affected.return_value = mock_citations

            result = get_rcw_cites_affected(bill_id, biennium)

            # Property 10: RCW Notation Formatting (consistency)
            assert result["success"] is True
            
            citations = result["data"]["rcw_citations"]["amended"]
            assert len(citations) == num_citations
            
            # All citations should follow the same format pattern
            for citation in citations:
                formatted = citation["citation"]
                
                # Must start with "RCW "
                assert formatted.startswith("RCW ")
                
                # Must have format "RCW X.Y" where X and Y are present
                parts = formatted.split(" ", 1)
                assert len(parts) == 2, f"Citation must have 'RCW ' prefix: {formatted}"
                
                rcw_part = parts[1]
                assert "." in rcw_part, f"Citation must have Chapter.Section format: {formatted}"

    @given(
        biennium=biennium_strategy,
        bill_id=bill_id_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_rcw_notation_with_complex_chapters(self, biennium, bill_id):
        """
        Feature: missing-api-coverage, Property 10: RCW Notation Formatting
        
        Test formatting with complex chapter numbers (e.g., "28A.150", "9.94A").
        """
        complex_chapters = [
            ("28A.150", "260"),
            ("9.94A", "030"),
            ("43.21C", "100"),
        ]
        
        mock_citations = [
            generate_mock_rcw_citation(chapter, section)
            for chapter, section in complex_chapters
        ]

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_rcw_cites_affected.return_value = mock_citations

            result = get_rcw_cites_affected(bill_id, biennium)

            # Property 10: RCW Notation Formatting (complex chapters)
            assert result["success"] is True
            
            citations = result["data"]["rcw_citations"]["amended"]
            assert len(citations) == len(complex_chapters)
            
            for i, citation in enumerate(citations):
                chapter, section = complex_chapters[i]
                expected = f"RCW {chapter}.{section}"
                
                assert citation["citation"] == expected, (
                    f"Expected '{expected}', got '{citation['citation']}'"
                )

    @given(
        biennium=biennium_strategy,
        bill_id=bill_id_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_rcw_notation_with_missing_section(self, biennium, bill_id):
        """
        Feature: missing-api-coverage, Property 10: RCW Notation Formatting
        
        Test formatting when section is missing (chapter only).
        """
        mock_citations = [
            {
                "rcw_chapter": "28A.150",
                "rcw_section": "",  # Missing section
                "action": "Amended",
            }
        ]

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_rcw_cites_affected.return_value = mock_citations

            result = get_rcw_cites_affected(bill_id, biennium)

            # Property 10: RCW Notation Formatting (missing section)
            assert result["success"] is True
            
            citations = result["data"]["rcw_citations"]["amended"]
            assert len(citations) == 1
            
            # Should still format with "RCW " prefix
            assert citations[0]["citation"].startswith("RCW ")
            # Should include the chapter
            assert "28A.150" in citations[0]["citation"]

    @given(
        biennium=biennium_strategy,
        bill_id=bill_id_strategy
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_rcw_notation_with_missing_chapter(self, biennium, bill_id):
        """
        Feature: missing-api-coverage, Property 10: RCW Notation Formatting
        
        Test formatting when chapter is missing (section only).
        """
        mock_citations = [
            {
                "rcw_chapter": "",  # Missing chapter
                "rcw_section": "260",
                "action": "Amended",
            }
        ]

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_rcw_cites_affected.return_value = mock_citations

            result = get_rcw_cites_affected(bill_id, biennium)

            # Property 10: RCW Notation Formatting (missing chapter)
            assert result["success"] is True
            
            citations = result["data"]["rcw_citations"]["amended"]
            assert len(citations) == 1
            
            # Should still format with "RCW " prefix
            assert citations[0]["citation"].startswith("RCW ")

    @given(
        biennium=biennium_strategy,
        bill_id=bill_id_strategy,
        num_citations=st.integers(min_value=1, max_value=10)
    )
    @settings(max_examples=100)
    @pytest.mark.property_test
    def test_rcw_notation_includes_chapter_and_section_fields(self, biennium, bill_id, num_citations):
        """
        Feature: missing-api-coverage, Property 10: RCW Notation Formatting
        
        Test that formatted citations include separate chapter and section fields.
        """
        mock_citations = []
        for i in range(num_citations):
            chapter = f"{10 + i}.{i}"
            section = f"{100 + i}"
            mock_citations.append(generate_mock_rcw_citation(chapter, section))

        with (
            patch("wa_leg_mcp.tools.rcw_tools.get_current_biennium") as mock_get_biennium,
            patch("wa_leg_mcp.tools.rcw_tools.wsl_client") as mock_client,
        ):
            mock_get_biennium.return_value = biennium
            mock_client.get_rcw_cites_affected.return_value = mock_citations

            result = get_rcw_cites_affected(bill_id, biennium)

            # Property 10: RCW Notation Formatting (separate fields)
            assert result["success"] is True
            
            citations = result["data"]["rcw_citations"]["amended"]
            
            for citation in citations:
                # Must have formatted citation
                assert "citation" in citation
                assert citation["citation"].startswith("RCW ")
                
                # Must also have separate chapter and section fields
                assert "chapter" in citation, "Must have separate 'chapter' field"
                assert "section" in citation, "Must have separate 'section' field"
                
                # Chapter and section should be in the formatted citation
                if citation["chapter"]:
                    assert citation["chapter"] in citation["citation"]
                if citation["section"]:
                    assert citation["section"] in citation["citation"]
