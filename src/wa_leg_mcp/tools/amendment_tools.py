"""
Amendment-related MCP tools for Washington State Legislature data.
"""

import logging
from typing import Any, Dict, Optional

from ..clients.wsl_client import WSLClient
from ..utils.formatters import get_current_biennium

logger = logging.getLogger(__name__)

wsl_client = WSLClient()


def get_amendments_for_biennium(
    bill_number: str, biennium: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve amendments for a specific bill in a biennium.

    This tool fetches all amendments proposed for a bill during a biennium, including
    amendment sponsor, description, status, and floor action information.

    Args:
        bill_number: Bill number in format "HB 1234" or "SB 5678" or just the number (e.g., "1234")
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing amendments with sponsor, status, and description.
        Returns empty list with descriptive message if no amendments exist.

    Example:
        >>> get_amendments_for_biennium("HB 1234", "2023-24")
        {
            "success": True,
            "data": {
                "bill_number": "HB 1234",
                "biennium": "2023-24",
                "amendments": [
                    {
                        "name": "1234-S AMH SMIT H2345.1",
                        "bill_id": "HB 1234",
                        "type": "Floor",
                        "floor_number": 1234,
                        "sponsor_name": "Smith",
                        "description": "Striker",
                        "drafter": "H2345.1",
                        "floor_action": "ADOPTED",
                        "floor_action_date": "2023-03-15",
                        "document_exists": True,
                        "htm_url": "http://...",
                        "pdf_url": "http://...",
                        "agency": "House"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetAmendmentsForBiennium",
                "count": 1
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
                    "tool_name": "get_amendments_for_biennium",
                    "api_call": "GetAmendmentsForBiennium",
                },
            }

        bill_num = int(bill_num_str)

        logger.info(f"Fetching amendments for bill {bill_num} in biennium {biennium}")

        # Call WSLClient to get amendment data
        amendments_data = wsl_client.get_amendments_for_biennium(biennium, bill_num)

        # Handle case where no amendments exist
        if not amendments_data or len(amendments_data) == 0:
            return {
                "success": True,
                "data": {
                    "bill_number": bill_number,
                    "biennium": biennium,
                    "amendments": [],
                },
                "metadata": {
                    "message": f"No amendments found for bill {bill_number} in biennium {biennium}",
                    "api_call": "GetAmendmentsForBiennium",
                },
            }

        # Parse and format amendment data
        formatted_amendments = []

        for amendment in amendments_data:
            formatted_amendments.append(
                {
                    "name": amendment.get("name", ""),
                    "bill_id": amendment.get("bill_id", ""),
                    "bill_number": amendment.get("bill_number", ""),
                    "legislative_session": amendment.get("legislative_session", ""),
                    "type": amendment.get("type", ""),
                    "floor_number": amendment.get("floor_number", ""),
                    "sponsor_name": amendment.get("sponsor_name", ""),
                    "description": amendment.get("description", ""),
                    "drafter": amendment.get("drafter", ""),
                    "floor_action": amendment.get("floor_action", ""),
                    "floor_action_date": str(amendment.get("floor_action_date", ""))
                    if amendment.get("floor_action_date")
                    else "",
                    "document_exists": amendment.get("document_exists", False),
                    "htm_url": amendment.get("htm_url", ""),
                    "pdf_url": amendment.get("pdf_url", ""),
                    "agency": amendment.get("agency", ""),
                }
            )

        return {
            "success": True,
            "data": {
                "bill_number": bill_number,
                "biennium": biennium,
                "amendments": formatted_amendments,
            },
            "metadata": {"api_call": "GetAmendmentsForBiennium", "count": len(formatted_amendments)},
        }

    except ValueError as e:
        logger.error(f"Invalid bill number format: {bill_number}")
        return {
            "success": False,
            "error": f"Invalid bill number: {bill_number}. Must be a valid number.",
            "error_type": "validation",
            "metadata": {
                "tool_name": "get_amendments_for_biennium",
                "api_call": "GetAmendmentsForBiennium",
            },
        }
    except Exception as e:
        logger.error(f"Error fetching amendments for bill {bill_number}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch amendments: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_amendments_for_biennium",
                "api_call": "GetAmendmentsForBiennium",
            },
        }



def get_amendments_for_year(bill_number: str, year: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve amendments for a specific bill in a year.

    This tool fetches all amendments proposed for a bill during a specific year.
    It accepts both 2-digit and 4-digit year formats for flexibility.

    Args:
        bill_number: Bill number in format "HB 1234" or "SB 5678" or just the number (e.g., "1234")
        year: Year in format "YYYY" or "YY" (e.g., "2023" or "23") (optional, defaults to current year)

    Returns:
        Dict containing amendments with sponsor, status, and description.
        Returns empty list with descriptive message if no amendments exist.

    Example:
        >>> get_amendments_for_year("HB 1234", "2023")
        {
            "success": True,
            "data": {
                "bill_number": "HB 1234",
                "year": "2023",
                "amendments": [...]
            },
            "metadata": {
                "api_call": "GetAmendmentsForYear",
                "count": 1
            }
        }
    """
    try:
        # Use current year if none provided
        if not year:
            biennium = get_current_biennium()
            year = biennium.split("-")[0]

        # Normalize year format - convert to integer
        year_str = year.strip()

        # Handle both 2-digit and 4-digit year formats
        if len(year_str) == 2:
            # 2-digit year - assume 20xx for years 00-99
            year_int = int(year_str)
            if year_int >= 0 and year_int <= 99:
                year_int = 2000 + year_int
            year_normalized = str(year_int)
        elif len(year_str) == 4:
            # 4-digit year
            year_int = int(year_str)
            year_normalized = year_str
        else:
            return {
                "success": False,
                "error": f"Invalid year format: {year}. Expected 2-digit (e.g., '23') or 4-digit (e.g., '2023') format.",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_amendments_for_year",
                    "api_call": "GetAmendmentsForYear",
                },
            }

        # Extract numeric bill number from input
        bill_num_str = bill_number.strip()
        if " " in bill_num_str:
            bill_num_str = bill_num_str.split()[-1]

        # Remove any non-numeric characters
        bill_num_str = "".join(c for c in bill_num_str if c.isdigit())

        if not bill_num_str:
            return {
                "success": False,
                "error": f"Invalid bill number format: {bill_number}. Expected format: 'HB 1234', 'SB 5678', or '1234'",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_amendments_for_year",
                    "api_call": "GetAmendmentsForYear",
                },
            }

        bill_num = int(bill_num_str)

        logger.info(f"Fetching amendments for bill {bill_num} in year {year_normalized}")

        # Call WSLClient to get amendment data
        amendments_data = wsl_client.get_amendments_for_year(year_int, bill_num)

        # Handle case where no amendments exist
        if not amendments_data or len(amendments_data) == 0:
            return {
                "success": True,
                "data": {
                    "bill_number": bill_number,
                    "year": year_normalized,
                    "amendments": [],
                },
                "metadata": {
                    "message": f"No amendments found for bill {bill_number} in year {year_normalized}",
                    "api_call": "GetAmendmentsForYear",
                },
            }

        # Parse and format amendment data
        formatted_amendments = []

        for amendment in amendments_data:
            formatted_amendments.append(
                {
                    "name": amendment.get("name", ""),
                    "bill_id": amendment.get("bill_id", ""),
                    "bill_number": amendment.get("bill_number", ""),
                    "legislative_session": amendment.get("legislative_session", ""),
                    "type": amendment.get("type", ""),
                    "floor_number": amendment.get("floor_number", ""),
                    "sponsor_name": amendment.get("sponsor_name", ""),
                    "description": amendment.get("description", ""),
                    "drafter": amendment.get("drafter", ""),
                    "floor_action": amendment.get("floor_action", ""),
                    "floor_action_date": str(amendment.get("floor_action_date", ""))
                    if amendment.get("floor_action_date")
                    else "",
                    "document_exists": amendment.get("document_exists", False),
                    "htm_url": amendment.get("htm_url", ""),
                    "pdf_url": amendment.get("pdf_url", ""),
                    "agency": amendment.get("agency", ""),
                }
            )

        return {
            "success": True,
            "data": {
                "bill_number": bill_number,
                "year": year_normalized,
                "amendments": formatted_amendments,
            },
            "metadata": {"api_call": "GetAmendmentsForYear", "count": len(formatted_amendments)},
        }

    except ValueError as e:
        logger.error(f"Invalid input format - bill: {bill_number}, year: {year}")
        return {
            "success": False,
            "error": f"Invalid input format. Bill number and year must be valid numbers.",
            "error_type": "validation",
            "metadata": {
                "tool_name": "get_amendments_for_year",
                "api_call": "GetAmendmentsForYear",
            },
        }
    except Exception as e:
        logger.error(f"Error fetching amendments for bill {bill_number} in year {year}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch amendments: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_amendments_for_year",
                "api_call": "GetAmendmentsForYear",
            },
        }
