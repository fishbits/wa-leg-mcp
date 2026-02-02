"""
Session law-related MCP tools for Washington State Legislature data.
"""

import logging
from typing import Any, Dict, Optional

from ..clients.wsl_client import WSLClient
from ..utils.formatters import get_current_biennium

logger = logging.getLogger(__name__)

wsl_client = WSLClient()


def get_session_law_by_bill(
    bill_number: str, biennium: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve session law information for a specific bill.

    This tool fetches session law data including chapter number, effective date,
    and law text reference for bills that have been enacted into law.

    Args:
        bill_number: Bill number in format "HB 1234" or "SB 5678" or just the number (e.g., "1234")
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing session law information with chapter number, effective date, and law text URL.
        Returns message if bill has not been enacted into law.

    Example:
        >>> get_session_law_by_bill("HB 1234", "2023-24")
        {
            "success": True,
            "data": {
                "bill_number": "HB 1234",
                "biennium": "2023-24",
                "session_law": {
                    "chapter": "123",
                    "year": "2023",
                    "session": "Regular",
                    "effective_date": "2023-07-23",
                    "law_text_url": "http://...",
                    "multiple_effective_dates": False
                }
            },
            "metadata": {
                "api_call": "GetSessionLawByBill"
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        # Extract numeric bill number from input (handle "HB 1234", "SB 5678", or "1234")
        bill_num_str = bill_number.strip()
        if " " in bill_num_str:
            # Format like "HB 1234" or "SB 5678"
            bill_num_str = bill_num_str.split()[-1]

        # Remove any non-numeric characters
        bill_num_str = "".join(c for c in bill_num_str if c.isdigit())

        if not bill_num_str:
            return {
                "success": False,
                "error": f"Invalid bill number format: {bill_number}. Expected format: 'HB 1234', 'SB 5678', or '1234'",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_session_law_by_bill",
                    "api_call": "GetSessionLawByBill",
                },
            }

        bill_num = int(bill_num_str)

        logger.info(f"Fetching session law for bill {bill_num} in biennium {biennium}")

        # Call WSLClient to get session law data
        session_law_data = wsl_client.get_session_law_by_bill(biennium, bill_num)

        # Handle case where bill has not been enacted into law
        if not session_law_data:
            return {
                "success": True,
                "data": {
                    "bill_number": bill_number,
                    "biennium": biennium,
                    "session_law": None,
                },
                "metadata": {
                    "message": f"Bill {bill_number} has not been enacted into law in biennium {biennium}",
                    "api_call": "GetSessionLawByBill",
                },
            }

        # Parse and format session law data
        formatted_session_law = {
            "chapter": session_law_data.get("chapter", ""),
            "year": str(session_law_data.get("year", "")) if session_law_data.get("year") else "",
            "session": session_law_data.get("session", ""),
            "effective_date": str(session_law_data.get("effective_date", ""))
            if session_law_data.get("effective_date")
            else "",
            "law_text_url": session_law_data.get("law_text_url", ""),
            "multiple_effective_dates": session_law_data.get("multiple_effective_dates", False),
            "partial_veto": session_law_data.get("partial_veto", False),
        }

        return {
            "success": True,
            "data": {
                "bill_number": bill_number,
                "biennium": biennium,
                "session_law": formatted_session_law,
            },
            "metadata": {"api_call": "GetSessionLawByBill"},
        }

    except ValueError as e:
        logger.error(f"Invalid bill number format: {bill_number}")
        return {
            "success": False,
            "error": f"Invalid bill number: {bill_number}. Must be a valid number.",
            "error_type": "validation",
            "metadata": {
                "tool_name": "get_session_law_by_bill",
                "api_call": "GetSessionLawByBill",
            },
        }
    except Exception as e:
        logger.error(f"Error fetching session law for bill {bill_number}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch session law: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_session_law_by_bill",
                "api_call": "GetSessionLawByBill",
            },
        }



def get_session_law_by_bill_id(
    bill_id: str, biennium: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve session law information by bill ID.

    This tool fetches session law data using the full bill ID (e.g., "HB 1234").

    Args:
        bill_id: Bill ID in format "HB 1234" or "SB 5678"
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing session law information with chapter number, effective date, and law text URL.
        Returns message if bill has not been enacted into law.

    Example:
        >>> get_session_law_by_bill_id("HB 1234", "2023-24")
        {
            "success": True,
            "data": {
                "bill_id": "HB 1234",
                "biennium": "2023-24",
                "session_law": {...}
            },
            "metadata": {
                "api_call": "GetSessionLawByBillId"
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        # Validate bill_id format
        bill_id_str = bill_id.strip()
        if not bill_id_str:
            return {
                "success": False,
                "error": "Bill ID cannot be empty",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_session_law_by_bill_id",
                    "api_call": "GetSessionLawByBillId",
                },
            }

        logger.info(f"Fetching session law for bill ID {bill_id_str} in biennium {biennium}")

        # Call WSLClient to get session law data
        session_law_data = wsl_client.get_session_law_by_bill_id(biennium, bill_id_str)

        # Handle case where bill has not been enacted into law
        if not session_law_data:
            return {
                "success": True,
                "data": {
                    "bill_id": bill_id_str,
                    "biennium": biennium,
                    "session_law": None,
                },
                "metadata": {
                    "message": f"Bill {bill_id_str} has not been enacted into law in biennium {biennium}",
                    "api_call": "GetSessionLawByBillId",
                },
            }

        # Parse and format session law data
        formatted_session_law = {
            "chapter": session_law_data.get("chapter", ""),
            "year": str(session_law_data.get("year", "")) if session_law_data.get("year") else "",
            "session": session_law_data.get("session", ""),
            "effective_date": str(session_law_data.get("effective_date", ""))
            if session_law_data.get("effective_date")
            else "",
            "law_text_url": session_law_data.get("law_text_url", ""),
            "multiple_effective_dates": session_law_data.get("multiple_effective_dates", False),
            "partial_veto": session_law_data.get("partial_veto", False),
        }

        return {
            "success": True,
            "data": {
                "bill_id": bill_id_str,
                "biennium": biennium,
                "session_law": formatted_session_law,
            },
            "metadata": {"api_call": "GetSessionLawByBillId"},
        }

    except Exception as e:
        logger.error(f"Error fetching session law for bill ID {bill_id}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch session law: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_session_law_by_bill_id",
                "api_call": "GetSessionLawByBillId",
            },
        }


def get_bill_by_chapter_number(
    year: str, chapter_number: str, session: int = 0
) -> Dict[str, Any]:
    """
    Retrieve bill information by session law chapter number (reverse lookup).

    This tool performs a reverse lookup from session law chapter number to bill information.

    Args:
        year: Year in format "YYYY" (e.g., "2023")
        chapter_number: Session law chapter number (e.g., "123")
        session: Session code (0=Regular, 1=1st Special, 2=2nd Special, etc.) (optional, defaults to 0)

    Returns:
        Dict containing bill information for the specified chapter.
        Returns message if no bill found for the chapter.

    Example:
        >>> get_bill_by_chapter_number("2023", "123")
        {
            "success": True,
            "data": {
                "year": "2023",
                "chapter_number": "123",
                "session": 0,
                "bill": {
                    "bill_id": "HB 1234",
                    "bill_number": 1234,
                    "short_description": "...",
                    ...
                }
            },
            "metadata": {
                "api_call": "GetBillByChapterNumber"
            }
        }
    """
    try:
        # Validate and parse year
        year_str = year.strip()
        if not year_str or not year_str.isdigit() or len(year_str) != 4:
            return {
                "success": False,
                "error": f"Invalid year format: {year}. Expected 4-digit year (e.g., '2023')",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_bill_by_chapter_number",
                    "api_call": "GetBillByChapterNumber",
                },
            }

        year_int = int(year_str)

        # Validate chapter number
        chapter_str = chapter_number.strip()
        if not chapter_str or not chapter_str.isdigit():
            return {
                "success": False,
                "error": f"Invalid chapter number format: {chapter_number}. Expected numeric value",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_bill_by_chapter_number",
                    "api_call": "GetBillByChapterNumber",
                },
            }

        chapter_int = int(chapter_str)

        logger.info(
            f"Fetching bill for chapter {chapter_int} in year {year_int} session {session}"
        )

        # Call WSLClient to get bill data
        bill_data = wsl_client.get_bill_by_chapter_number(year_int, session, chapter_int)

        # Handle case where no bill found
        if not bill_data:
            return {
                "success": True,
                "data": {
                    "year": year_str,
                    "chapter_number": chapter_str,
                    "session": session,
                    "bill": None,
                },
                "metadata": {
                    "message": f"No bill found for chapter {chapter_str} in year {year_str} session {session}",
                    "api_call": "GetBillByChapterNumber",
                },
            }

        # Return formatted bill data
        return {
            "success": True,
            "data": {
                "year": year_str,
                "chapter_number": chapter_str,
                "session": session,
                "bill": bill_data,
            },
            "metadata": {"api_call": "GetBillByChapterNumber"},
        }

    except ValueError as e:
        logger.error(f"Invalid input format - year: {year}, chapter: {chapter_number}")
        return {
            "success": False,
            "error": f"Invalid input format. Year and chapter number must be valid numbers.",
            "error_type": "validation",
            "metadata": {
                "tool_name": "get_bill_by_chapter_number",
                "api_call": "GetBillByChapterNumber",
            },
        }
    except Exception as e:
        logger.error(
            f"Error fetching bill for chapter {chapter_number} in year {year}: {str(e)}"
        )
        return {
            "success": False,
            "error": f"Failed to fetch bill: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_bill_by_chapter_number",
                "api_call": "GetBillByChapterNumber",
            },
        }


def get_chapter_numbers_by_year(year: str) -> Dict[str, Any]:
    """
    Retrieve all session law chapters for a specific year.

    This tool fetches all session laws enacted in a given year.

    Args:
        year: Year in format "YYYY" (e.g., "2023")

    Returns:
        Dict containing list of all session law chapters for the year.
        Returns empty list if no session laws found.

    Example:
        >>> get_chapter_numbers_by_year("2023")
        {
            "success": True,
            "data": {
                "year": "2023",
                "chapters": [
                    {
                        "chapter": "1",
                        "bill_id": "HB 1001",
                        "effective_date": "2023-07-23",
                        ...
                    },
                    ...
                ]
            },
            "metadata": {
                "api_call": "GetChapterNumbersByYear",
                "count": 150
            }
        }
    """
    try:
        # Validate and parse year
        year_str = year.strip()
        if not year_str or not year_str.isdigit() or len(year_str) != 4:
            return {
                "success": False,
                "error": f"Invalid year format: {year}. Expected 4-digit year (e.g., '2023')",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_chapter_numbers_by_year",
                    "api_call": "GetChapterNumbersByYear",
                },
            }

        year_int = int(year_str)

        logger.info(f"Fetching chapter numbers for year {year_int}")

        # Call WSLClient to get chapter data
        chapters_data = wsl_client.get_chapter_numbers_by_year(year_int)

        # Handle case where no chapters found
        if not chapters_data or len(chapters_data) == 0:
            return {
                "success": True,
                "data": {
                    "year": year_str,
                    "chapters": [],
                },
                "metadata": {
                    "message": f"No session law chapters found for year {year_str}",
                    "api_call": "GetChapterNumbersByYear",
                    "count": 0,
                },
            }

        return {
            "success": True,
            "data": {
                "year": year_str,
                "chapters": chapters_data,
            },
            "metadata": {
                "api_call": "GetChapterNumbersByYear",
                "count": len(chapters_data),
            },
        }

    except ValueError as e:
        logger.error(f"Invalid year format: {year}")
        return {
            "success": False,
            "error": f"Invalid year: {year}. Must be a valid 4-digit year.",
            "error_type": "validation",
            "metadata": {
                "tool_name": "get_chapter_numbers_by_year",
                "api_call": "GetChapterNumbersByYear",
            },
        }
    except Exception as e:
        logger.error(f"Error fetching chapter numbers for year {year}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch chapter numbers: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_chapter_numbers_by_year",
                "api_call": "GetChapterNumbersByYear",
            },
        }


def get_session_law_by_initiative_number(initiative_number: str) -> Dict[str, Any]:
    """
    Retrieve session law information for an initiative.

    This tool fetches session law data for initiatives (citizen-initiated legislation).

    Args:
        initiative_number: Initiative number (e.g., "1234" for I-1234)

    Returns:
        Dict containing session law information for the initiative.
        Returns message if initiative has not been enacted into law.

    Example:
        >>> get_session_law_by_initiative_number("1234")
        {
            "success": True,
            "data": {
                "initiative_number": "1234",
                "session_law": {
                    "chapter": "50",
                    "year": "2023",
                    "effective_date": "2023-12-07",
                    ...
                }
            },
            "metadata": {
                "api_call": "GetSessionLawByInitiativeNumber"
            }
        }
    """
    try:
        # Validate initiative number
        initiative_str = initiative_number.strip()
        if not initiative_str or not initiative_str.isdigit():
            return {
                "success": False,
                "error": f"Invalid initiative number format: {initiative_number}. Expected numeric value",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_session_law_by_initiative_number",
                    "api_call": "GetSessionLawByInitiativeNumber",
                },
            }

        initiative_int = int(initiative_str)

        logger.info(f"Fetching session law for initiative {initiative_int}")

        # Call WSLClient to get session law data
        session_law_data = wsl_client.get_session_law_by_initiative_number(initiative_int)

        # Handle case where initiative has not been enacted into law
        if not session_law_data:
            return {
                "success": True,
                "data": {
                    "initiative_number": initiative_str,
                    "session_law": None,
                },
                "metadata": {
                    "message": f"Initiative {initiative_str} has not been enacted into law",
                    "api_call": "GetSessionLawByInitiativeNumber",
                },
            }

        # Parse and format session law data
        formatted_session_law = {
            "chapter": session_law_data.get("chapter", ""),
            "year": str(session_law_data.get("year", "")) if session_law_data.get("year") else "",
            "session": session_law_data.get("session", ""),
            "effective_date": str(session_law_data.get("effective_date", ""))
            if session_law_data.get("effective_date")
            else "",
            "law_text_url": session_law_data.get("law_text_url", ""),
            "multiple_effective_dates": session_law_data.get("multiple_effective_dates", False),
            "partial_veto": session_law_data.get("partial_veto", False),
        }

        return {
            "success": True,
            "data": {
                "initiative_number": initiative_str,
                "session_law": formatted_session_law,
            },
            "metadata": {"api_call": "GetSessionLawByInitiativeNumber"},
        }

    except ValueError as e:
        logger.error(f"Invalid initiative number format: {initiative_number}")
        return {
            "success": False,
            "error": f"Invalid initiative number: {initiative_number}. Must be a valid number.",
            "error_type": "validation",
            "metadata": {
                "tool_name": "get_session_law_by_initiative_number",
                "api_call": "GetSessionLawByInitiativeNumber",
            },
        }
    except Exception as e:
        logger.error(f"Error fetching session law for initiative {initiative_number}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch session law: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_session_law_by_initiative_number",
                "api_call": "GetSessionLawByInitiativeNumber",
            },
        }
