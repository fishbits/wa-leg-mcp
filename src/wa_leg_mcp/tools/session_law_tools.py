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
