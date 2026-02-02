"""
Governor action-related MCP tools for Washington State Legislature data.
"""

import logging
from typing import Any, Dict, Optional

from ..clients.wsl_client import WSLClient
from ..utils.formatters import get_current_biennium

logger = logging.getLogger(__name__)

wsl_client = WSLClient()


def get_legislation_governor_signed(biennium: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve bills signed by the governor.

    This tool fetches all bills that were signed by the governor during a biennium,
    including action dates and bill information.

    Args:
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of signed bills with action dates.
        Returns empty list with descriptive message if no signed bills found.

    Example:
        >>> get_legislation_governor_signed("2023-24")
        {
            "success": True,
            "data": {
                "biennium": "2023-24",
                "signed_bills": [
                    {
                        "bill_id": "HB 1234",
                        "bill_number": 1234,
                        "short_description": "...",
                        "action_date": "2023-05-15",
                        ...
                    }
                ]
            },
            "metadata": {
                "api_call": "GetLegislationGovernorSigned",
                "count": 150
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching governor signed bills for biennium {biennium}")

        # Call WSLClient for both House and Senate bills
        house_bills = wsl_client.get_legislation_governor_signed(biennium, "House")
        senate_bills = wsl_client.get_legislation_governor_signed(biennium, "Senate")

        # Combine results
        all_signed_bills = []
        if house_bills:
            all_signed_bills.extend(house_bills)
        if senate_bills:
            all_signed_bills.extend(senate_bills)

        # Handle case where no signed bills found
        if not all_signed_bills or len(all_signed_bills) == 0:
            return {
                "success": True,
                "data": {
                    "biennium": biennium,
                    "signed_bills": [],
                },
                "metadata": {
                    "message": f"No bills signed by governor found for biennium {biennium}",
                    "api_call": "GetLegislationGovernorSigned",
                    "count": 0,
                },
            }

        return {
            "success": True,
            "data": {
                "biennium": biennium,
                "signed_bills": all_signed_bills,
            },
            "metadata": {
                "api_call": "GetLegislationGovernorSigned",
                "count": len(all_signed_bills),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching governor signed bills for biennium {biennium}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch governor signed bills: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_legislation_governor_signed",
                "api_call": "GetLegislationGovernorSigned",
            },
        }


def get_legislation_governor_veto(biennium: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve bills vetoed by the governor.

    This tool fetches all bills that were vetoed by the governor during a biennium,
    including veto messages and action dates.

    Args:
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of vetoed bills with veto messages.
        Returns empty list with descriptive message if no vetoed bills found.

    Example:
        >>> get_legislation_governor_veto("2023-24")
        {
            "success": True,
            "data": {
                "biennium": "2023-24",
                "vetoed_bills": [
                    {
                        "bill_id": "SB 5678",
                        "bill_number": 5678,
                        "short_description": "...",
                        "veto_message": "...",
                        "action_date": "2023-05-20",
                        ...
                    }
                ]
            },
            "metadata": {
                "api_call": "GetLegislationGovernorVeto",
                "count": 5
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching governor vetoed bills for biennium {biennium}")

        # Call WSLClient for both House and Senate bills
        house_bills = wsl_client.get_legislation_governor_veto(biennium, "House")
        senate_bills = wsl_client.get_legislation_governor_veto(biennium, "Senate")

        # Combine results
        all_vetoed_bills = []
        if house_bills:
            all_vetoed_bills.extend(house_bills)
        if senate_bills:
            all_vetoed_bills.extend(senate_bills)

        # Handle case where no vetoed bills found
        if not all_vetoed_bills or len(all_vetoed_bills) == 0:
            return {
                "success": True,
                "data": {
                    "biennium": biennium,
                    "vetoed_bills": [],
                },
                "metadata": {
                    "message": f"No bills vetoed by governor found for biennium {biennium}",
                    "api_call": "GetLegislationGovernorVeto",
                    "count": 0,
                },
            }

        return {
            "success": True,
            "data": {
                "biennium": biennium,
                "vetoed_bills": all_vetoed_bills,
            },
            "metadata": {
                "api_call": "GetLegislationGovernorVeto",
                "count": len(all_vetoed_bills),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching governor vetoed bills for biennium {biennium}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch governor vetoed bills: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_legislation_governor_veto",
                "api_call": "GetLegislationGovernorVeto",
            },
        }


def get_legislation_governor_partial_veto(biennium: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve bills partially vetoed by the governor.

    This tool fetches all bills that received line-item vetoes from the governor
    during a biennium, including information about affected sections.

    Args:
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of partially vetoed bills with affected sections.
        Returns empty list with descriptive message if no partially vetoed bills found.

    Example:
        >>> get_legislation_governor_partial_veto("2023-24")
        {
            "success": True,
            "data": {
                "biennium": "2023-24",
                "partial_veto_bills": [
                    {
                        "bill_id": "HB 2000",
                        "bill_number": 2000,
                        "short_description": "...",
                        "partial_veto_message": "...",
                        "action_date": "2023-05-25",
                        ...
                    }
                ]
            },
            "metadata": {
                "api_call": "GetLegislationGovernorPartialVeto",
                "count": 3
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching governor partially vetoed bills for biennium {biennium}")

        # Call WSLClient for both House and Senate bills
        house_bills = wsl_client.get_legislation_governor_partial_veto(biennium, "House")
        senate_bills = wsl_client.get_legislation_governor_partial_veto(biennium, "Senate")

        # Combine results
        all_partial_veto_bills = []
        if house_bills:
            all_partial_veto_bills.extend(house_bills)
        if senate_bills:
            all_partial_veto_bills.extend(senate_bills)

        # Handle case where no partially vetoed bills found
        if not all_partial_veto_bills or len(all_partial_veto_bills) == 0:
            return {
                "success": True,
                "data": {
                    "biennium": biennium,
                    "partial_veto_bills": [],
                },
                "metadata": {
                    "message": f"No bills partially vetoed by governor found for biennium {biennium}",
                    "api_call": "GetLegislationGovernorPartialVeto",
                    "count": 0,
                },
            }

        return {
            "success": True,
            "data": {
                "biennium": biennium,
                "partial_veto_bills": all_partial_veto_bills,
            },
            "metadata": {
                "api_call": "GetLegislationGovernorPartialVeto",
                "count": len(all_partial_veto_bills),
            },
        }

    except Exception as e:
        logger.error(
            f"Error fetching governor partially vetoed bills for biennium {biennium}: {str(e)}"
        )
        return {
            "success": False,
            "error": f"Failed to fetch governor partially vetoed bills: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_legislation_governor_partial_veto",
                "api_call": "GetLegislationGovernorPartialVeto",
            },
        }
