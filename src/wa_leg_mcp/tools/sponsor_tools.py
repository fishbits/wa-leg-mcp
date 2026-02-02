"""
Enhanced sponsor information MCP tools for Washington State Legislature data.

This module provides tools for retrieving detailed sponsor information including
sponsors from both chambers and entities authorized to request legislation.
"""

import logging
from typing import Any, Dict

from ..clients.wsl_client import WSLClient
from ..utils.formatters import get_current_biennium

logger = logging.getLogger(__name__)

wsl_client = WSLClient()


def get_sponsors(biennium: str = None) -> Dict[str, Any]:
    """
    Retrieve all sponsors for a biennium from both chambers.

    This tool fetches sponsor information for both House and Senate,
    including names, party affiliation, district, and contact information.

    Args:
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of sponsors with metadata.
        Returns empty list with descriptive message if no sponsors exist.

    Example:
        >>> get_sponsors("2023-24")
        {
            "success": True,
            "data": {
                "biennium": "2023-24",
                "sponsors": [
                    {
                        "id": "123",
                        "name": "John Doe",
                        "party": "D",
                        "district": "43",
                        "agency": "House",
                        "phone": "(360) 786-7100",
                        "email": "john.doe@leg.wa.gov"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetSponsors",
                "count": 1
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching all sponsors for biennium {biennium}")

        # Call WSLClient to get sponsors
        sponsors_data = wsl_client.get_sponsors(biennium)

        # Handle case where no sponsors exist
        if not sponsors_data or len(sponsors_data) == 0:
            return {
                "success": True,
                "data": {"biennium": biennium, "sponsors": []},
                "metadata": {
                    "message": f"No sponsors found for biennium {biennium}",
                    "api_call": "GetSponsors",
                    "count": 0,
                },
            }

        # Format sponsor data
        formatted_sponsors = []
        for sponsor in sponsors_data:
            formatted_sponsors.append(
                {
                    "id": sponsor.get("id", ""),
                    "name": sponsor.get("name", ""),
                    "long_name": sponsor.get("long_name", ""),
                    "party": sponsor.get("party", ""),
                    "district": sponsor.get("district", ""),
                    "agency": sponsor.get("agency", ""),
                    "phone": sponsor.get("phone", ""),
                    "email": sponsor.get("email", ""),
                    "first_name": sponsor.get("first_name", ""),
                    "last_name": sponsor.get("last_name", ""),
                }
            )

        return {
            "success": True,
            "data": {"biennium": biennium, "sponsors": formatted_sponsors},
            "metadata": {
                "api_call": "GetSponsors",
                "count": len(formatted_sponsors),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching sponsors: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch sponsors: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_sponsors",
                "api_call": "GetSponsors",
            },
        }


def get_house_sponsors(biennium: str = None) -> Dict[str, Any]:
    """
    Retrieve House sponsors for a biennium.

    This tool fetches sponsor information for the House of Representatives,
    including names, party affiliation, district, and contact information.

    Args:
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of House sponsors with metadata.
        Returns empty list with descriptive message if no sponsors exist.

    Example:
        >>> get_house_sponsors("2023-24")
        {
            "success": True,
            "data": {
                "biennium": "2023-24",
                "sponsors": [
                    {
                        "id": "123",
                        "name": "John Doe",
                        "party": "D",
                        "district": "43",
                        "agency": "House",
                        "phone": "(360) 786-7100",
                        "email": "john.doe@leg.wa.gov"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetHouseSponsors",
                "count": 1
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching House sponsors for biennium {biennium}")

        # Call WSLClient to get House sponsors
        sponsors_data = wsl_client.get_house_sponsors(biennium)

        # Handle case where no sponsors exist
        if not sponsors_data or len(sponsors_data) == 0:
            return {
                "success": True,
                "data": {"biennium": biennium, "sponsors": []},
                "metadata": {
                    "message": f"No House sponsors found for biennium {biennium}",
                    "api_call": "GetHouseSponsors",
                    "count": 0,
                },
            }

        # Format sponsor data
        formatted_sponsors = []
        for sponsor in sponsors_data:
            formatted_sponsors.append(
                {
                    "id": sponsor.get("id", ""),
                    "name": sponsor.get("name", ""),
                    "long_name": sponsor.get("long_name", ""),
                    "party": sponsor.get("party", ""),
                    "district": sponsor.get("district", ""),
                    "agency": sponsor.get("agency", ""),
                    "phone": sponsor.get("phone", ""),
                    "email": sponsor.get("email", ""),
                    "first_name": sponsor.get("first_name", ""),
                    "last_name": sponsor.get("last_name", ""),
                }
            )

        return {
            "success": True,
            "data": {"biennium": biennium, "sponsors": formatted_sponsors},
            "metadata": {
                "api_call": "GetHouseSponsors",
                "count": len(formatted_sponsors),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching House sponsors: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch House sponsors: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_house_sponsors",
                "api_call": "GetHouseSponsors",
            },
        }


def get_senate_sponsors(biennium: str = None) -> Dict[str, Any]:
    """
    Retrieve Senate sponsors for a biennium.

    This tool fetches sponsor information for the Senate,
    including names, party affiliation, district, and contact information.

    Args:
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of Senate sponsors with metadata.
        Returns empty list with descriptive message if no sponsors exist.

    Example:
        >>> get_senate_sponsors("2023-24")
        {
            "success": True,
            "data": {
                "biennium": "2023-24",
                "sponsors": [
                    {
                        "id": "456",
                        "name": "Jane Smith",
                        "party": "R",
                        "district": "5",
                        "agency": "Senate",
                        "phone": "(360) 786-7715",
                        "email": "jane.smith@leg.wa.gov"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetSenateSponsors",
                "count": 1
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching Senate sponsors for biennium {biennium}")

        # Call WSLClient to get Senate sponsors
        sponsors_data = wsl_client.get_senate_sponsors(biennium)

        # Handle case where no sponsors exist
        if not sponsors_data or len(sponsors_data) == 0:
            return {
                "success": True,
                "data": {"biennium": biennium, "sponsors": []},
                "metadata": {
                    "message": f"No Senate sponsors found for biennium {biennium}",
                    "api_call": "GetSenateSponsors",
                    "count": 0,
                },
            }

        # Format sponsor data
        formatted_sponsors = []
        for sponsor in sponsors_data:
            formatted_sponsors.append(
                {
                    "id": sponsor.get("id", ""),
                    "name": sponsor.get("name", ""),
                    "long_name": sponsor.get("long_name", ""),
                    "party": sponsor.get("party", ""),
                    "district": sponsor.get("district", ""),
                    "agency": sponsor.get("agency", ""),
                    "phone": sponsor.get("phone", ""),
                    "email": sponsor.get("email", ""),
                    "first_name": sponsor.get("first_name", ""),
                    "last_name": sponsor.get("last_name", ""),
                }
            )

        return {
            "success": True,
            "data": {"biennium": biennium, "sponsors": formatted_sponsors},
            "metadata": {
                "api_call": "GetSenateSponsors",
                "count": len(formatted_sponsors),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching Senate sponsors: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch Senate sponsors: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_senate_sponsors",
                "api_call": "GetSenateSponsors",
            },
        }


def get_requesters(biennium: str = None) -> Dict[str, Any]:
    """
    Retrieve entities authorized to request legislation for a biennium.

    This tool fetches information about entities (agencies, departments, etc.)
    that are authorized to request legislation.

    Args:
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of requesters with metadata.
        Returns empty list with descriptive message if no requesters exist.

    Example:
        >>> get_requesters("2023-24")
        {
            "success": True,
            "data": {
                "biennium": "2023-24",
                "requesters": [
                    {
                        "id": "789",
                        "name": "Department of Transportation",
                        "type": "Agency"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetRequesters",
                "count": 1
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching requesters for biennium {biennium}")

        # Call WSLClient to get requesters
        requesters_data = wsl_client.get_requesters(biennium)

        # Handle case where no requesters exist
        if not requesters_data or len(requesters_data) == 0:
            return {
                "success": True,
                "data": {"biennium": biennium, "requesters": []},
                "metadata": {
                    "message": f"No requesters found for biennium {biennium}",
                    "api_call": "GetRequesters",
                    "count": 0,
                },
            }

        # Format requester data
        formatted_requesters = []
        for requester in requesters_data:
            formatted_requesters.append(
                {
                    "id": requester.get("id", ""),
                    "name": requester.get("name", ""),
                    "type": requester.get("type", ""),
                }
            )

        return {
            "success": True,
            "data": {"biennium": biennium, "requesters": formatted_requesters},
            "metadata": {
                "api_call": "GetRequesters",
                "count": len(formatted_requesters),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching requesters: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch requesters: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_requesters",
                "api_call": "GetRequesters",
            },
        }
