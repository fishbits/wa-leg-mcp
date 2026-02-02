"""
Property-based tests for session law retrieval tools.

These tests validate correctness properties for session law tools using
property-based testing with hypothesis.
"""

import pytest
from hypothesis import given, strategies as st, assume
from unittest.mock import patch

from src.wa_leg_mcp.tools.session_law_tools import (
    get_session_law_by_bill,
    get_bill_by_chapter_number,
    get_chapter_numbers_by_year,
    get_session_law_by_initiative_number,
)


# Test data strategies
bienniums = st.sampled_from(["2021-22", "2023-24", "2025-26"])
bill_numbers = st.integers(min_value=1000, max_value=9999)
years = st.sampled_from(["2021", "2022", "2023", "2024", "2025"])
chapter_numbers = st.integers(min_value=1, max_value=500)
initiative_numbers = st.integers(min_value=1000, max_value=2000)


@pytest.mark.property_test
class TestSessionLawRetrievalProperties:
    """
    Property 16: Session Law Retrieval by Bill
    
    For any enacted bill, calling getSessionLawByBill SHALL return the chapter number,
    effective date, and law text reference.
    
    **Validates: Requirements 5.1**
    """

    @given(biennium=bienniums, bill_number=bill_numbers)
    def test_session_law_by_bill_structure(self, biennium, bill_number):
        """Test that session law retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock_client:
            # Mock enacted bill
            mock_client.get_session_law_by_bill.return_value = {
                "chapter": "123",
                "year": 2023,
                "session": "Regular",
                "effective_date": "2023-07-23",
                "law_text_url": "http://example.com/law.pdf",
                "multiple_effective_dates": False,
                "partial_veto": False,
            }

            result = get_session_law_by_bill(str(bill_number), biennium)

            # Verify response structure
            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"] and result["data"]["session_law"]:
                session_law = result["data"]["session_law"]
                # Verify required fields
                assert "chapter" in session_law
                assert "year" in session_law
                assert "effective_date" in session_law
                assert "law_text_url" in session_law

    @given(biennium=bienniums, bill_number=bill_numbers)
    def test_session_law_by_bill_not_enacted_handling(self, biennium, bill_number):
        """Test that bills not enacted return None with descriptive message."""
        with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock_client:
            # Mock bill not enacted
            mock_client.get_session_law_by_bill.return_value = None

            result = get_session_law_by_bill(str(bill_number), biennium)

            # Verify response structure for non-enacted bills
            assert result["success"] is True
            assert result["data"]["session_law"] is None
            assert "message" in result["metadata"]
            assert "not been enacted" in result["metadata"]["message"]

    @given(biennium=bienniums, bill_number=bill_numbers)
    def test_session_law_by_bill_includes_partial_veto_flag(self, biennium, bill_number):
        """Test that session law includes partial veto information."""
        with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock_client:
            # Mock bill with partial veto
            mock_client.get_session_law_by_bill.return_value = {
                "chapter": "200",
                "year": 2023,
                "session": "Regular",
                "effective_date": "2023-07-23",
                "law_text_url": "http://example.com/law.pdf",
                "multiple_effective_dates": False,
                "partial_veto": True,
            }

            result = get_session_law_by_bill(str(bill_number), biennium)

            if result["success"] and result["data"]["session_law"]:
                assert "partial_veto" in result["data"]["session_law"]

    @given(biennium=bienniums, bill_number=bill_numbers)
    def test_session_law_by_bill_includes_multiple_effective_dates_flag(
        self, biennium, bill_number
    ):
        """Test that session law includes multiple effective dates flag."""
        with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock_client:
            # Mock bill with multiple effective dates
            mock_client.get_session_law_by_bill.return_value = {
                "chapter": "300",
                "year": 2023,
                "session": "Regular",
                "effective_date": "2023-07-23",
                "law_text_url": "http://example.com/law.pdf",
                "multiple_effective_dates": True,
                "partial_veto": False,
            }

            result = get_session_law_by_bill(str(bill_number), biennium)

            if result["success"] and result["data"]["session_law"]:
                assert "multiple_effective_dates" in result["data"]["session_law"]


@pytest.mark.property_test
class TestSessionLawReverseLookupProperties:
    """
    Property 17: Session Law Reverse Lookup
    
    For any valid chapter number and year, calling getBillByChapterNumber SHALL
    return the corresponding bill information.
    
    **Validates: Requirements 5.2**
    """

    @given(year=years, chapter_number=chapter_numbers)
    def test_bill_by_chapter_number_structure(self, year, chapter_number):
        """Test that reverse lookup returns proper structure."""
        with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock_client:
            # Mock bill data
            mock_client.get_bill_by_chapter_number.return_value = {
                "bill_id": "HB 1234",
                "bill_number": 1234,
                "short_description": "Test bill",
                "biennium": "2023-24",
            }

            result = get_bill_by_chapter_number(year, str(chapter_number))

            # Verify response structure
            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"] and result["data"]["bill"]:
                bill = result["data"]["bill"]
                # Verify bill data is present
                assert "bill_id" in bill or "bill_number" in bill

    @given(year=years, chapter_number=chapter_numbers)
    def test_bill_by_chapter_number_not_found_handling(self, year, chapter_number):
        """Test that invalid chapter numbers return None with message."""
        with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock_client:
            # Mock chapter not found
            mock_client.get_bill_by_chapter_number.return_value = None

            result = get_bill_by_chapter_number(year, str(chapter_number))

            # Verify response structure for not found
            assert result["success"] is True
            assert result["data"]["bill"] is None
            assert "message" in result["metadata"]
            assert "No bill found" in result["metadata"]["message"]

    @given(year=years, chapter_number=chapter_numbers, session=st.integers(min_value=0, max_value=3))
    def test_bill_by_chapter_number_session_parameter(self, year, chapter_number, session):
        """Test that session parameter is properly handled."""
        with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock_client:
            mock_client.get_bill_by_chapter_number.return_value = {
                "bill_id": "SB 5678",
                "bill_number": 5678,
            }

            result = get_bill_by_chapter_number(year, str(chapter_number), session=session)

            # Verify session is included in response
            assert result["data"]["session"] == session


@pytest.mark.property_test
class TestAnnualSessionLawCompletenessProperties:
    """
    Property 18: Annual Session Law Completeness
    
    For any year, calling getChapterNumbersByYear SHALL return all session laws
    enacted during that year.
    
    **Validates: Requirements 5.3**
    """

    @given(year=years)
    def test_chapter_numbers_by_year_structure(self, year):
        """Test that annual chapter retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock_client:
            # Mock chapter data
            mock_client.get_chapter_numbers_by_year.return_value = [
                {"chapter": "1", "bill_id": "HB 1001"},
                {"chapter": "2", "bill_id": "SB 5001"},
            ]

            result = get_chapter_numbers_by_year(year)

            # Verify response structure
            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"]:
                assert "chapters" in result["data"]
                assert "count" in result["metadata"]
                assert isinstance(result["data"]["chapters"], list)

    @given(year=years)
    def test_chapter_numbers_by_year_empty_handling(self, year):
        """Test that years with no chapters return empty list with message."""
        with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock_client:
            # Mock no chapters
            mock_client.get_chapter_numbers_by_year.return_value = []

            result = get_chapter_numbers_by_year(year)

            # Verify response structure for empty results
            assert result["success"] is True
            assert result["data"]["chapters"] == []
            assert result["metadata"]["count"] == 0
            assert "message" in result["metadata"]

    @given(year=years, num_chapters=st.integers(min_value=0, max_value=200))
    def test_chapter_numbers_by_year_count_matches_list_length(self, year, num_chapters):
        """Test that count metadata matches actual list length."""
        with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock_client:
            # Mock varying number of chapters
            mock_chapters = [{"chapter": str(i), "bill_id": f"HB {1000+i}"} for i in range(num_chapters)]
            mock_client.get_chapter_numbers_by_year.return_value = mock_chapters

            result = get_chapter_numbers_by_year(year)

            if result["success"]:
                assert result["metadata"]["count"] == len(result["data"]["chapters"])


@pytest.mark.property_test
class TestInitiativeSessionLawRetrievalProperties:
    """
    Property 19: Initiative Session Law Retrieval
    
    For any initiative number and year, calling getSessionLawByInitiativeNumber SHALL
    return initiative-specific session law data.
    
    **Validates: Requirements 5.4**
    """

    @given(initiative_number=initiative_numbers)
    def test_session_law_by_initiative_structure(self, initiative_number):
        """Test that initiative session law retrieval returns proper structure."""
        with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock_client:
            # Mock initiative session law
            mock_client.get_session_law_by_initiative_number.return_value = {
                "chapter": "50",
                "year": 2023,
                "session": "Regular",
                "effective_date": "2023-12-07",
                "law_text_url": "http://example.com/initiative.pdf",
                "multiple_effective_dates": False,
                "partial_veto": False,
            }

            result = get_session_law_by_initiative_number(str(initiative_number))

            # Verify response structure
            assert "success" in result
            assert "data" in result
            assert "metadata" in result

            if result["success"] and result["data"]["session_law"]:
                session_law = result["data"]["session_law"]
                # Verify required fields
                assert "chapter" in session_law
                assert "year" in session_law
                assert "effective_date" in session_law

    @given(initiative_number=initiative_numbers)
    def test_session_law_by_initiative_not_enacted_handling(self, initiative_number):
        """Test that initiatives not enacted return None with message."""
        with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock_client:
            # Mock initiative not enacted
            mock_client.get_session_law_by_initiative_number.return_value = None

            result = get_session_law_by_initiative_number(str(initiative_number))

            # Verify response structure for non-enacted initiatives
            assert result["success"] is True
            assert result["data"]["session_law"] is None
            assert "message" in result["metadata"]
            assert "not been enacted" in result["metadata"]["message"]

    @given(initiative_number=initiative_numbers)
    def test_session_law_by_initiative_includes_all_fields(self, initiative_number):
        """Test that initiative session law includes all expected fields."""
        with patch("src.wa_leg_mcp.tools.session_law_tools.wsl_client") as mock_client:
            # Mock complete initiative session law
            mock_client.get_session_law_by_initiative_number.return_value = {
                "chapter": "75",
                "year": 2023,
                "session": "Regular",
                "effective_date": "2023-12-07",
                "law_text_url": "http://example.com/initiative.pdf",
                "multiple_effective_dates": True,
                "partial_veto": False,
            }

            result = get_session_law_by_initiative_number(str(initiative_number))

            if result["success"] and result["data"]["session_law"]:
                session_law = result["data"]["session_law"]
                # Verify all expected fields are present
                assert "chapter" in session_law
                assert "year" in session_law
                assert "session" in session_law
                assert "effective_date" in session_law
                assert "law_text_url" in session_law
                assert "multiple_effective_dates" in session_law
                assert "partial_veto" in session_law
