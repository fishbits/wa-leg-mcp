"""
Committee-related MCP tools for Washington State Legislature data.
"""

import logging
from typing import Any, Dict

from ..clients.wsl_client import WSLClient
from ..utils.formatters import get_current_biennium

logger = logging.getLogger(__name__)

wsl_client = WSLClient()


def get_committee_meetings(start_date: str, end_date: str, committee: str = None) -> Dict[str, Any]:
    """
    Retrieve committee meetings and agendas.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        committee: Filter by specific committee (optional)

    Returns:
        Dict containing list of committee meetings
    """
    try:
        logger.info(f"Fetching committee meetings from {start_date} to {end_date}")

        # Get committee meetings
        meetings_data = wsl_client.get_committee_meetings(start_date, end_date)

        if not meetings_data or len(meetings_data) == 0:
            return {"error": f"No meetings found between {start_date} and {end_date}"}

        # Filter by committee if specified
        filtered_meetings = []

        for meeting in meetings_data:
            # Check if committee matches any of the committees in the meeting
            if committee and not any(
                c.get("name", "").lower() == committee.lower()
                for c in meeting.get("committees", [])
            ):
                continue

            committees_info = [
                {
                    "name": c.get("name", ""),
                    "long_name": c.get("long_name", ""),
                    "agency": c.get("agency", ""),
                    "acronym": c.get("acronym", ""),
                    "id": c.get("id", ""),
                }
                for c in meeting.get("committees", [])
            ]

            filtered_meetings.append(
                {
                    "agenda_id": meeting.get("agenda_id", ""),
                    "agency": meeting.get("agency", ""),
                    "committees": committees_info,
                    "date": meeting.get("date", ""),
                    "room": meeting.get("room", ""),
                    "building": meeting.get("building", ""),
                    "cancelled": meeting.get("cancelled", False),
                    "committee_type": meeting.get("committee_type", ""),
                    "notes": meeting.get("notes", ""),
                    "address": meeting.get("address", ""),
                    "city": meeting.get("city", ""),
                    "state": meeting.get("state", ""),
                }
            )

        return {
            "start_date": start_date,
            "end_date": end_date,
            "count": len(filtered_meetings),
            "meetings": filtered_meetings,
        }

    except Exception as e:
        logger.error(f"Error fetching committee meetings: {str(e)}")
        return {"error": f"Failed to fetch committee meetings: {str(e)}"}


def get_committees(biennium: str = None) -> Dict[str, Any]:
    """
    Retrieve list of committees for a specific biennium.

    Args:
        biennium: Legislative biennium in format "2025-26" (optional, defaults to current)

    Returns:
        Dict containing list of committees
    """
    try:
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching committees for biennium {biennium}")

        # Get committees
        committees_data = wsl_client.get_committees(biennium)

        if not committees_data or len(committees_data) == 0:
            return {"error": f"No committees found for biennium {biennium}"}

        formatted_committees = []
        for committee in committees_data:
            formatted_committees.append(
                {
                    "id": committee.get("id", ""),
                    "name": committee.get("name", ""),
                    "long_name": committee.get("long_name", ""),
                    "agency": committee.get("agency", ""),
                    "acronym": committee.get("acronym", ""),
                    "phone": committee.get("phone", ""),
                }
            )

        return {
            "biennium": biennium,
            "count": len(formatted_committees),
            "committees": formatted_committees,
        }

    except Exception as e:
        logger.error(f"Error fetching committees: {str(e)}")
        return {"error": f"Failed to fetch committees: {str(e)}"}



def get_hearings(bill_number: str, biennium: str = None) -> Dict[str, Any]:
    """
    Retrieve committee hearings for a specific bill.

    This tool fetches all scheduled and past committee hearings for a bill,
    including committee name, date, time, location, and agenda items.

    Args:
        bill_number: Bill number in format "HB 1234" or "SB 5678" or just the number (e.g., "1234")
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing hearings with committee, date, time, location, and agenda.
        Returns empty list with descriptive message if no hearings exist.

    Example:
        >>> get_hearings("HB 1234", "2023-24")
        {
            "success": True,
            "data": {
                "bill_number": "HB 1234",
                "biennium": "2023-24",
                "hearings": [
                    {
                        "agenda_id": 12345,
                        "committee": {
                            "name": "Education",
                            "long_name": "House Committee on Education",
                            "agency": "House"
                        },
                        "date": "2023-03-15T10:00:00",
                        "room": "John L. O'Brien Building Hearing Room A",
                        "building": "John L. O'Brien Building",
                        "cancelled": False,
                        "revised": False,
                        "committee_type": "Full Committee",
                        "notes": "Public hearing and possible executive action."
                    }
                ]
            },
            "metadata": {
                "api_call": "GetHearings",
                "count": 1
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

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
                    "tool_name": "get_hearings",
                    "api_call": "GetHearings",
                },
            }

        bill_num = int(bill_num_str)

        logger.info(f"Fetching hearings for bill {bill_num} in biennium {biennium}")

        # Call WSLClient to get hearing data
        hearings_data = wsl_client.get_hearings(biennium, bill_num)

        # Handle case where no hearings exist
        if not hearings_data or len(hearings_data) == 0:
            return {
                "success": True,
                "data": {
                    "bill_number": bill_number,
                    "biennium": biennium,
                    "hearings": [],
                },
                "metadata": {
                    "message": f"No hearings found for bill {bill_number} in biennium {biennium}",
                    "api_call": "GetHearings",
                },
            }

        # Parse and format hearing data
        formatted_hearings = []

        for hearing in hearings_data:
            # Extract committee information
            committees = hearing.get("committees", [])
            committee_info = None
            if committees and len(committees) > 0:
                first_committee = committees[0]
                committee_info = {
                    "id": first_committee.get("id", ""),
                    "name": first_committee.get("name", ""),
                    "long_name": first_committee.get("long_name", ""),
                    "agency": first_committee.get("agency", ""),
                    "acronym": first_committee.get("acronym", ""),
                }

            # Check if meeting was revised
            revised_date = hearing.get("revised_date")
            is_revised = False
            if revised_date:
                # Check if revised_date is not the default datetime(1, 1, 1, 0, 0)
                revised_str = str(revised_date)
                is_revised = not revised_str.startswith("0001-01-01")

            formatted_hearings.append(
                {
                    "agenda_id": hearing.get("agenda_id", ""),
                    "committee": committee_info,
                    "date": str(hearing.get("date", "")) if hearing.get("date") else "",
                    "room": hearing.get("room", ""),
                    "building": hearing.get("building", ""),
                    "address": hearing.get("address", ""),
                    "city": hearing.get("city", ""),
                    "state": hearing.get("state", ""),
                    "cancelled": hearing.get("cancelled", False),
                    "revised": is_revised,
                    "committee_type": hearing.get("committee_type", ""),
                    "notes": hearing.get("notes", ""),
                }
            )

        # Sort hearings by date (chronological order)
        formatted_hearings.sort(key=lambda x: x.get("date", ""))

        return {
            "success": True,
            "data": {
                "bill_number": bill_number,
                "biennium": biennium,
                "hearings": formatted_hearings,
            },
            "metadata": {"api_call": "GetHearings", "count": len(formatted_hearings)},
        }

    except ValueError as e:
        logger.error(f"Invalid bill number format: {bill_number}")
        return {
            "success": False,
            "error": f"Invalid bill number: {bill_number}. Must be a valid number.",
            "error_type": "validation",
            "metadata": {
                "tool_name": "get_hearings",
                "api_call": "GetHearings",
            },
        }
    except Exception as e:
        logger.error(f"Error fetching hearings for bill {bill_number}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch hearings: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_hearings",
                "api_call": "GetHearings",
            },
        }
