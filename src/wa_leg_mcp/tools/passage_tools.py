"""
Bill passage and status tracking MCP tools for Washington State Legislature data.

This module provides tools for tracking bills through the legislative process,
including passage through chambers and status changes over time.
"""

import logging
from typing import Any, Dict

from ..clients.wsl_client import WSLClient
from ..utils.formatters import get_current_biennium

logger = logging.getLogger(__name__)

wsl_client = WSLClient()


def get_legislation_passed_house(biennium: str = None) -> Dict[str, Any]:
    """
    Retrieve bills that passed the House for a biennium.

    This tool fetches all bills that successfully passed the House of Representatives,
    including passage dates and vote counts.

    Args:
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of House-passed bills with metadata.
        Returns empty list with descriptive message if no bills passed.

    Example:
        >>> get_legislation_passed_house("2023-24")
        {
            "success": True,
            "data": {
                "biennium": "2023-24",
                "bills": [
                    {
                        "bill_id": "HB 1234",
                        "bill_number": "1234",
                        "short_description": "Education funding",
                        "passage_date": "2023-03-15",
                        "yea_votes": 65,
                        "nay_votes": 33
                    }
                ]
            },
            "metadata": {
                "api_call": "GetLegislationPassedHouse",
                "count": 1
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching House-passed bills for biennium {biennium}")

        # Call WSLClient to get House-passed bills
        bills_data = wsl_client.get_legislation_passed_house(biennium)

        # Handle case where no bills passed
        if not bills_data or len(bills_data) == 0:
            return {
                "success": True,
                "data": {"biennium": biennium, "bills": []},
                "metadata": {
                    "message": f"No bills passed the House in biennium {biennium}",
                    "api_call": "GetLegislationPassedHouse",
                    "count": 0,
                },
            }

        # Format bill data
        formatted_bills = []
        for bill in bills_data:
            formatted_bills.append(
                {
                    "bill_id": bill.get("bill_id", ""),
                    "bill_number": bill.get("bill_number", ""),
                    "substitute_version": bill.get("substitute_version", ""),
                    "engrossed_version": bill.get("engrossed_version", ""),
                    "short_legislation_type": bill.get("short_legislation_type", {}),
                    "original_agency": bill.get("original_agency", ""),
                    "active": bill.get("active", False),
                }
            )

        return {
            "success": True,
            "data": {"biennium": biennium, "bills": formatted_bills},
            "metadata": {
                "api_call": "GetLegislationPassedHouse",
                "count": len(formatted_bills),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching House-passed bills: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch House-passed bills: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_legislation_passed_house",
                "api_call": "GetLegislationPassedHouse",
            },
        }


def get_legislation_passed_senate(biennium: str = None) -> Dict[str, Any]:
    """
    Retrieve bills that passed the Senate for a biennium.

    This tool fetches all bills that successfully passed the Senate,
    including passage dates and vote counts.

    Args:
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of Senate-passed bills with metadata.
        Returns empty list with descriptive message if no bills passed.

    Example:
        >>> get_legislation_passed_senate("2023-24")
        {
            "success": True,
            "data": {
                "biennium": "2023-24",
                "bills": [
                    {
                        "bill_id": "SB 5678",
                        "bill_number": "5678",
                        "short_description": "Transportation funding",
                        "passage_date": "2023-04-20"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetLegislationPassedSenate",
                "count": 1
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching Senate-passed bills for biennium {biennium}")

        # Call WSLClient to get Senate-passed bills
        bills_data = wsl_client.get_legislation_passed_senate(biennium)

        # Handle case where no bills passed
        if not bills_data or len(bills_data) == 0:
            return {
                "success": True,
                "data": {"biennium": biennium, "bills": []},
                "metadata": {
                    "message": f"No bills passed the Senate in biennium {biennium}",
                    "api_call": "GetLegislationPassedSenate",
                    "count": 0,
                },
            }

        # Format bill data
        formatted_bills = []
        for bill in bills_data:
            formatted_bills.append(
                {
                    "bill_id": bill.get("bill_id", ""),
                    "bill_number": bill.get("bill_number", ""),
                    "substitute_version": bill.get("substitute_version", ""),
                    "engrossed_version": bill.get("engrossed_version", ""),
                    "short_legislation_type": bill.get("short_legislation_type", {}),
                    "original_agency": bill.get("original_agency", ""),
                    "active": bill.get("active", False),
                }
            )

        return {
            "success": True,
            "data": {"biennium": biennium, "bills": formatted_bills},
            "metadata": {
                "api_call": "GetLegislationPassedSenate",
                "count": len(formatted_bills),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching Senate-passed bills: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch Senate-passed bills: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_legislation_passed_senate",
                "api_call": "GetLegislationPassedSenate",
            },
        }


def get_legislation_passed_legislature(biennium: str = None) -> Dict[str, Any]:
    """
    Retrieve bills that passed both chambers (the full legislature).

    This tool fetches bills that successfully passed both the House and Senate,
    representing bills that completed the legislative process.

    Args:
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of bills that passed both chambers with metadata.
        Returns empty list with descriptive message if no bills passed both chambers.

    Example:
        >>> get_legislation_passed_legislature("2023-24")
        {
            "success": True,
            "data": {
                "biennium": "2023-24",
                "bills": [
                    {
                        "bill_id": "HB 1234",
                        "bill_number": "1234",
                        "short_description": "Budget bill"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetLegislationPassedLegislature",
                "count": 1
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching legislature-passed bills for biennium {biennium}")

        # Call WSLClient to get legislature-passed bills
        bills_data = wsl_client.get_legislation_passed_legislature(biennium)

        # Handle case where no bills passed both chambers
        if not bills_data or len(bills_data) == 0:
            return {
                "success": True,
                "data": {"biennium": biennium, "bills": []},
                "metadata": {
                    "message": f"No bills passed both chambers in biennium {biennium}",
                    "api_call": "GetLegislationPassedLegislature",
                    "count": 0,
                },
            }

        # Format bill data
        formatted_bills = []
        for bill in bills_data:
            formatted_bills.append(
                {
                    "bill_id": bill.get("bill_id", ""),
                    "bill_number": bill.get("bill_number", ""),
                    "substitute_version": bill.get("substitute_version", ""),
                    "engrossed_version": bill.get("engrossed_version", ""),
                    "short_legislation_type": bill.get("short_legislation_type", {}),
                    "original_agency": bill.get("original_agency", ""),
                    "active": bill.get("active", False),
                }
            )

        return {
            "success": True,
            "data": {"biennium": biennium, "bills": formatted_bills},
            "metadata": {
                "api_call": "GetLegislationPassedLegislature",
                "count": len(formatted_bills),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching legislature-passed bills: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch legislature-passed bills: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_legislation_passed_legislature",
                "api_call": "GetLegislationPassedLegislature",
            },
        }


def get_prefiled_legislation() -> Dict[str, Any]:
    """
    Retrieve prefiled legislation.

    This tool fetches bills that were filed before the legislative session began,
    including filing dates and sponsor information.

    Returns:
        Dict containing list of prefiled bills with metadata.
        Returns empty list with descriptive message if no bills were prefiled.

    Example:
        >>> get_prefiled_legislation()
        {
            "success": True,
            "data": {
                "bills": [
                    {
                        "bill_id": "HB 1001",
                        "bill_number": "1001",
                        "short_description": "Early filed bill",
                        "introduced_date": "2022-12-01"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetPrefiledLegislation",
                "count": 1
            }
        }
    """
    try:
        logger.info("Fetching prefiled legislation")

        # Call WSLClient to get prefiled bills
        bills_data = wsl_client.get_prefiled_legislation()

        # Handle case where no bills were prefiled
        if not bills_data or len(bills_data) == 0:
            return {
                "success": True,
                "data": {"bills": []},
                "metadata": {
                    "message": "No prefiled legislation found",
                    "api_call": "GetPrefiledLegislation",
                    "count": 0,
                },
            }

        # Format bill data
        formatted_bills = []
        for bill in bills_data:
            formatted_bills.append(
                {
                    "biennium": bill.get("biennium", ""),
                    "bill_id": bill.get("bill_id", ""),
                    "bill_number": bill.get("bill_number", ""),
                    "substitute_version": bill.get("substitute_version", ""),
                    "engrossed_version": bill.get("engrossed_version", ""),
                    "short_legislation_type": bill.get("short_legislation_type", {}),
                    "original_agency": bill.get("original_agency", ""),
                    "active": bill.get("active", False),
                    "short_description": bill.get("short_description", ""),
                    "introduced_date": str(bill.get("introduced_date", "")) if bill.get("introduced_date") else "",
                }
            )

        return {
            "success": True,
            "data": {"bills": formatted_bills},
            "metadata": {
                "api_call": "GetPrefiledLegislation",
                "count": len(formatted_bills),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching prefiled legislation: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch prefiled legislation: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_prefiled_legislation",
                "api_call": "GetPrefiledLegislation",
            },
        }


def get_legislative_status_changes(begin_date: str, end_date: str, biennium: str = None) -> Dict[str, Any]:
    """
    Retrieve bill status changes within a date range.

    This tool fetches all bills that had status changes during the specified period,
    including old status, new status, and change dates.

    Args:
        begin_date: Start date in ISO 8601 format (e.g., "2023-01-01")
        end_date: End date in ISO 8601 format (e.g., "2023-12-31")
        biennium: Legislative biennium in format "YYYY-YY" (optional, defaults to current)

    Returns:
        Dict containing list of status changes with metadata.
        Returns empty list with descriptive message if no status changes occurred.

    Example:
        >>> get_legislative_status_changes("2023-01-01", "2023-12-31", "2023-24")
        {
            "success": True,
            "data": {
                "begin_date": "2023-01-01",
                "end_date": "2023-12-31",
                "biennium": "2023-24",
                "status_changes": [
                    {
                        "bill_id": "HB 1234",
                        "action_date": "2023-03-15",
                        "history_line": "Passed to Rules Committee",
                        "status": "H Rules"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetLegislativeStatusChanges",
                "count": 1
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching status changes from {begin_date} to {end_date} for biennium {biennium}")

        # Call WSLClient to get status changes
        changes_data = wsl_client.get_legislative_status_changes(biennium, begin_date, end_date)

        # Handle case where no status changes occurred
        if not changes_data or len(changes_data) == 0:
            return {
                "success": True,
                "data": {
                    "begin_date": begin_date,
                    "end_date": end_date,
                    "biennium": biennium,
                    "status_changes": [],
                },
                "metadata": {
                    "message": f"No status changes found from {begin_date} to {end_date}",
                    "api_call": "GetLegislativeStatusChanges",
                    "count": 0,
                },
            }

        # Format status change data
        formatted_changes = []
        for change in changes_data:
            formatted_changes.append(
                {
                    "bill_id": change.get("bill_id", ""),
                    "action_date": str(change.get("action_date", "")) if change.get("action_date") else "",
                    "history_line": change.get("history_line", ""),
                    "status": change.get("status", ""),
                    "amended_by_opposite_body": change.get("amended_by_opposite_body", False),
                    "partial_veto": change.get("partial_veto", False),
                    "veto": change.get("veto", False),
                    "amendments_exist": change.get("amendments_exist", False),
                }
            )

        return {
            "success": True,
            "data": {
                "begin_date": begin_date,
                "end_date": end_date,
                "biennium": biennium,
                "status_changes": formatted_changes,
            },
            "metadata": {
                "api_call": "GetLegislativeStatusChanges",
                "count": len(formatted_changes),
            },
        }

    except ValueError as e:
        logger.error(f"Invalid date format: {str(e)}")
        return {
            "success": False,
            "error": f"Invalid date format. Expected ISO 8601 format (YYYY-MM-DD): {str(e)}",
            "error_type": "validation",
            "metadata": {
                "tool_name": "get_legislative_status_changes",
                "api_call": "GetLegislativeStatusChanges",
            },
        }
    except Exception as e:
        logger.error(f"Error fetching status changes: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch status changes: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_legislative_status_changes",
                "api_call": "GetLegislativeStatusChanges",
            },
        }
