"""
Committee action-related MCP tools for Washington State Legislature data.
"""

import logging
from typing import Any, Dict, Optional

from ..clients.wsl_client import WSLClient
from ..utils.formatters import get_current_biennium

logger = logging.getLogger(__name__)

wsl_client = WSLClient()


def get_committee_executive_actions_by_bill(
    bill_number: str, biennium: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve executive actions taken on a bill by committees.

    This tool fetches all executive actions (e.g., "Do Pass", "Do Not Pass", "Without Recommendation")
    taken by committees on a specific bill.

    Args:
        bill_number: Bill number in format "HB 1234" or "SB 5678" or just the number (e.g., "1234")
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing executive actions with committee, date, and action type.
        Returns empty list with descriptive message if no actions found.

    Example:
        >>> get_committee_executive_actions_by_bill("HB 1234", "2023-24")
        {
            "success": True,
            "data": {
                "bill_number": "HB 1234",
                "biennium": "2023-24",
                "executive_actions": [
                    {
                        "committee_name": "House Finance",
                        "action_date": "2023-02-15",
                        "action": "Do Pass",
                        ...
                    }
                ]
            },
            "metadata": {
                "api_call": "GetCommitteeExecutiveActionsByBill",
                "count": 2
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

        bill_num_str = "".join(c for c in bill_num_str if c.isdigit())

        if not bill_num_str:
            return {
                "success": False,
                "error": f"Invalid bill number format: {bill_number}. Expected format: 'HB 1234', 'SB 5678', or '1234'",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_committee_executive_actions_by_bill",
                    "api_call": "GetCommitteeExecutiveActionsByBill",
                },
            }

        bill_num = int(bill_num_str)

        logger.info(
            f"Fetching committee executive actions for bill {bill_num} in biennium {biennium}"
        )

        # Call WSLClient to get executive actions
        actions_data = wsl_client.get_committee_executive_actions_by_bill(biennium, bill_num)

        # Handle case where no actions found
        if not actions_data or len(actions_data) == 0:
            return {
                "success": True,
                "data": {
                    "bill_number": bill_number,
                    "biennium": biennium,
                    "executive_actions": [],
                },
                "metadata": {
                    "message": f"No committee executive actions found for bill {bill_number} in biennium {biennium}",
                    "api_call": "GetCommitteeExecutiveActionsByBill",
                    "count": 0,
                },
            }

        return {
            "success": True,
            "data": {
                "bill_number": bill_number,
                "biennium": biennium,
                "executive_actions": actions_data,
            },
            "metadata": {
                "api_call": "GetCommitteeExecutiveActionsByBill",
                "count": len(actions_data),
            },
        }

    except ValueError as e:
        logger.error(f"Invalid bill number format: {bill_number}")
        return {
            "success": False,
            "error": f"Invalid bill number: {bill_number}. Must be a valid number.",
            "error_type": "validation",
            "metadata": {
                "tool_name": "get_committee_executive_actions_by_bill",
                "api_call": "GetCommitteeExecutiveActionsByBill",
            },
        }
    except Exception as e:
        logger.error(
            f"Error fetching committee executive actions for bill {bill_number}: {str(e)}"
        )
        return {
            "success": False,
            "error": f"Failed to fetch committee executive actions: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_committee_executive_actions_by_bill",
                "api_call": "GetCommitteeExecutiveActionsByBill",
            },
        }


def get_committee_referrals_by_bill(
    bill_number: str, biennium: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve committee referrals for a bill.

    This tool fetches the history of committee referrals for a specific bill,
    showing which committees the bill was referred to and when.

    Args:
        bill_number: Bill number in format "HB 1234" or "SB 5678" or just the number (e.g., "1234")
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing referral history with committees and dates.
        Returns empty list with descriptive message if no referrals found.

    Example:
        >>> get_committee_referrals_by_bill("SB 5678", "2023-24")
        {
            "success": True,
            "data": {
                "bill_number": "SB 5678",
                "biennium": "2023-24",
                "referrals": [
                    {
                        "committee_name": "Senate Ways & Means",
                        "referral_date": "2023-01-20",
                        ...
                    }
                ]
            },
            "metadata": {
                "api_call": "GetCommitteeReferralsByBill",
                "count": 3
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

        bill_num_str = "".join(c for c in bill_num_str if c.isdigit())

        if not bill_num_str:
            return {
                "success": False,
                "error": f"Invalid bill number format: {bill_number}. Expected format: 'HB 1234', 'SB 5678', or '1234'",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_committee_referrals_by_bill",
                    "api_call": "GetCommitteeReferralsByBill",
                },
            }

        bill_num = int(bill_num_str)

        logger.info(f"Fetching committee referrals for bill {bill_num} in biennium {biennium}")

        # Call WSLClient to get referrals
        referrals_data = wsl_client.get_committee_referrals_by_bill(biennium, bill_num)

        # Handle case where no referrals found
        if not referrals_data or len(referrals_data) == 0:
            return {
                "success": True,
                "data": {
                    "bill_number": bill_number,
                    "biennium": biennium,
                    "referrals": [],
                },
                "metadata": {
                    "message": f"No committee referrals found for bill {bill_number} in biennium {biennium}",
                    "api_call": "GetCommitteeReferralsByBill",
                    "count": 0,
                },
            }

        return {
            "success": True,
            "data": {
                "bill_number": bill_number,
                "biennium": biennium,
                "referrals": referrals_data,
            },
            "metadata": {
                "api_call": "GetCommitteeReferralsByBill",
                "count": len(referrals_data),
            },
        }

    except ValueError as e:
        logger.error(f"Invalid bill number format: {bill_number}")
        return {
            "success": False,
            "error": f"Invalid bill number: {bill_number}. Must be a valid number.",
            "error_type": "validation",
            "metadata": {
                "tool_name": "get_committee_referrals_by_bill",
                "api_call": "GetCommitteeReferralsByBill",
            },
        }
    except Exception as e:
        logger.error(f"Error fetching committee referrals for bill {bill_number}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch committee referrals: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_committee_referrals_by_bill",
                "api_call": "GetCommitteeReferralsByBill",
            },
        }


def get_committee_referrals_by_committee(
    committee_name: str, agency: str, biennium: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve bills referred to a specific committee.

    This tool fetches all bills that have been referred to a particular committee.

    Args:
        committee_name: Committee name (e.g., "Finance", "Ways & Means")
        agency: Chamber - "House" or "Senate"
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of bills referred to the committee.
        Returns empty list with descriptive message if no referrals found.

    Example:
        >>> get_committee_referrals_by_committee("Finance", "House", "2023-24")
        {
            "success": True,
            "data": {
                "committee_name": "Finance",
                "agency": "House",
                "biennium": "2023-24",
                "referred_bills": [...]
            },
            "metadata": {
                "api_call": "GetCommitteeReferralsByCommittee",
                "count": 45
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        # Validate agency
        if agency not in ["House", "Senate"]:
            return {
                "success": False,
                "error": f"Invalid agency: {agency}. Must be 'House' or 'Senate'",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_committee_referrals_by_committee",
                    "api_call": "GetCommitteeReferralsByCommittee",
                },
            }

        logger.info(
            f"Fetching bills referred to {agency} {committee_name} in biennium {biennium}"
        )

        # Call WSLClient to get referrals
        referrals_data = wsl_client.get_committee_referrals_by_committee(
            biennium, agency, committee_name
        )

        # Handle case where no referrals found
        if not referrals_data or len(referrals_data) == 0:
            return {
                "success": True,
                "data": {
                    "committee_name": committee_name,
                    "agency": agency,
                    "biennium": biennium,
                    "referred_bills": [],
                },
                "metadata": {
                    "message": f"No bills referred to {agency} {committee_name} in biennium {biennium}",
                    "api_call": "GetCommitteeReferralsByCommittee",
                    "count": 0,
                },
            }

        return {
            "success": True,
            "data": {
                "committee_name": committee_name,
                "agency": agency,
                "biennium": biennium,
                "referred_bills": referrals_data,
            },
            "metadata": {
                "api_call": "GetCommitteeReferralsByCommittee",
                "count": len(referrals_data),
            },
        }

    except Exception as e:
        logger.error(
            f"Error fetching referrals for {agency} {committee_name}: {str(e)}"
        )
        return {
            "success": False,
            "error": f"Failed to fetch committee referrals: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_committee_referrals_by_committee",
                "api_call": "GetCommitteeReferralsByCommittee",
            },
        }


def get_do_pass_by_committee(
    committee_name: str, agency: str, biennium: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve bills with "do pass" recommendation from a committee.

    This tool fetches bills that received a "do pass" recommendation from a specific committee.

    Args:
        committee_name: Committee name (e.g., "Finance", "Ways & Means")
        agency: Chamber - "House" or "Senate"
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of bills with do pass recommendation.
        Returns empty list with descriptive message if no bills found.

    Example:
        >>> get_do_pass_by_committee("Ways & Means", "Senate", "2023-24")
        {
            "success": True,
            "data": {
                "committee_name": "Ways & Means",
                "agency": "Senate",
                "biennium": "2023-24",
                "do_pass_bills": [...]
            },
            "metadata": {
                "api_call": "GetDoPassByCommittee",
                "count": 28
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        # Validate agency
        if agency not in ["House", "Senate"]:
            return {
                "success": False,
                "error": f"Invalid agency: {agency}. Must be 'House' or 'Senate'",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_do_pass_by_committee",
                    "api_call": "GetDoPassByCommittee",
                },
            }

        logger.info(
            f"Fetching do pass bills from {agency} {committee_name} in biennium {biennium}"
        )

        # Call WSLClient to get do pass bills
        bills_data = wsl_client.get_do_pass_by_committee(biennium, agency, committee_name)

        # Handle case where no bills found
        if not bills_data or len(bills_data) == 0:
            return {
                "success": True,
                "data": {
                    "committee_name": committee_name,
                    "agency": agency,
                    "biennium": biennium,
                    "do_pass_bills": [],
                },
                "metadata": {
                    "message": f"No do pass bills from {agency} {committee_name} in biennium {biennium}",
                    "api_call": "GetDoPassByCommittee",
                    "count": 0,
                },
            }

        return {
            "success": True,
            "data": {
                "committee_name": committee_name,
                "agency": agency,
                "biennium": biennium,
                "do_pass_bills": bills_data,
            },
            "metadata": {
                "api_call": "GetDoPassByCommittee",
                "count": len(bills_data),
            },
        }

    except Exception as e:
        logger.error(
            f"Error fetching do pass bills from {agency} {committee_name}: {str(e)}"
        )
        return {
            "success": False,
            "error": f"Failed to fetch do pass bills: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_do_pass_by_committee",
                "api_call": "GetDoPassByCommittee",
            },
        }


def get_in_committee(
    committee_name: str, agency: str, biennium: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve bills currently in a committee.

    This tool fetches all bills that are currently referred to a specific committee.

    Args:
        committee_name: Committee name (e.g., "Finance", "Ways & Means")
        agency: Chamber - "House" or "Senate"
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of bills currently in the committee.
        Returns empty list with descriptive message if no bills found.

    Example:
        >>> get_in_committee("Education", "House", "2023-24")
        {
            "success": True,
            "data": {
                "committee_name": "Education",
                "agency": "House",
                "biennium": "2023-24",
                "bills_in_committee": [...]
            },
            "metadata": {
                "api_call": "GetInCommittee",
                "count": 12
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        # Validate agency
        if agency not in ["House", "Senate"]:
            return {
                "success": False,
                "error": f"Invalid agency: {agency}. Must be 'House' or 'Senate'",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_in_committee",
                    "api_call": "GetInCommittee",
                },
            }

        logger.info(
            f"Fetching bills in {agency} {committee_name} for biennium {biennium}"
        )

        # Call WSLClient to get bills in committee
        bills_data = wsl_client.get_in_committee(biennium, agency, committee_name)

        # Handle case where no bills found
        if not bills_data or len(bills_data) == 0:
            return {
                "success": True,
                "data": {
                    "committee_name": committee_name,
                    "agency": agency,
                    "biennium": biennium,
                    "bills_in_committee": [],
                },
                "metadata": {
                    "message": f"No bills currently in {agency} {committee_name} for biennium {biennium}",
                    "api_call": "GetInCommittee",
                    "count": 0,
                },
            }

        return {
            "success": True,
            "data": {
                "committee_name": committee_name,
                "agency": agency,
                "biennium": biennium,
                "bills_in_committee": bills_data,
            },
            "metadata": {
                "api_call": "GetInCommittee",
                "count": len(bills_data),
            },
        }

    except Exception as e:
        logger.error(
            f"Error fetching bills in {agency} {committee_name}: {str(e)}"
        )
        return {
            "success": False,
            "error": f"Failed to fetch bills in committee: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_in_committee",
                "api_call": "GetInCommittee",
            },
        }


def get_legislation_reported_out_of_committee(
    committee_name: str, agency: str, begin_date: str, end_date: str
) -> Dict[str, Any]:
    """
    Retrieve bills reported out of a committee.

    This tool fetches bills that were reported out of a committee within a date range,
    including recommendation type and vote counts.

    Args:
        committee_name: Committee name (e.g., "Finance", "Ways & Means")
        agency: Chamber - "House" or "Senate"
        begin_date: Begin date in ISO 8601 format (e.g., "2023-01-01")
        end_date: End date in ISO 8601 format (e.g., "2023-12-31")

    Returns:
        Dict containing list of bills reported out with recommendations and votes.
        Returns empty list with descriptive message if no bills found.

    Example:
        >>> get_legislation_reported_out_of_committee("Finance", "House", "2023-01-01", "2023-12-31")
        {
            "success": True,
            "data": {
                "committee_name": "Finance",
                "agency": "House",
                "begin_date": "2023-01-01",
                "end_date": "2023-12-31",
                "reported_bills": [...]
            },
            "metadata": {
                "api_call": "GetLegislationReportedOutOfCommittee",
                "count": 35
            }
        }
    """
    try:
        # Validate agency
        if agency not in ["House", "Senate"]:
            return {
                "success": False,
                "error": f"Invalid agency: {agency}. Must be 'House' or 'Senate'",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_legislation_reported_out_of_committee",
                    "api_call": "GetLegislationReportedOutOfCommittee",
                },
            }

        logger.info(
            f"Fetching bills reported out of {agency} {committee_name} from {begin_date} to {end_date}"
        )

        # Call WSLClient to get reported bills
        bills_data = wsl_client.get_legislation_reported_out_of_committee(
            committee_name, agency, begin_date, end_date
        )

        # Handle case where no bills found
        if not bills_data or len(bills_data) == 0:
            return {
                "success": True,
                "data": {
                    "committee_name": committee_name,
                    "agency": agency,
                    "begin_date": begin_date,
                    "end_date": end_date,
                    "reported_bills": [],
                },
                "metadata": {
                    "message": f"No bills reported out of {agency} {committee_name} from {begin_date} to {end_date}",
                    "api_call": "GetLegislationReportedOutOfCommittee",
                    "count": 0,
                },
            }

        return {
            "success": True,
            "data": {
                "committee_name": committee_name,
                "agency": agency,
                "begin_date": begin_date,
                "end_date": end_date,
                "reported_bills": bills_data,
            },
            "metadata": {
                "api_call": "GetLegislationReportedOutOfCommittee",
                "count": len(bills_data),
            },
        }

    except Exception as e:
        logger.error(
            f"Error fetching bills reported out of {agency} {committee_name}: {str(e)}"
        )
        return {
            "success": False,
            "error": f"Failed to fetch reported bills: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_legislation_reported_out_of_committee",
                "api_call": "GetLegislationReportedOutOfCommittee",
            },
        }
