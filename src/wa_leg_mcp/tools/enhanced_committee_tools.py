"""
Enhanced committee information MCP tools for Washington State Legislature data.

This module provides tools for retrieving detailed committee information including
active committees, committee members, and historical committee composition.
"""

import logging
from typing import Any, Dict

from ..clients.wsl_client import WSLClient
from ..utils.formatters import get_current_biennium

logger = logging.getLogger(__name__)

wsl_client = WSLClient()


def get_active_committees() -> Dict[str, Any]:
    """
    Retrieve all currently active committees for both chambers.

    This tool fetches active committees from both the House and Senate,
    including committee names, acronyms, phone numbers, and agency information.

    Returns:
        Dict containing list of active committees with metadata.
        Returns empty list with descriptive message if no committees exist.

    Example:
        >>> get_active_committees()
        {
            "success": True,
            "data": {
                "committees": [
                    {
                        "id": "123",
                        "name": "Education",
                        "long_name": "House Committee on Education",
                        "agency": "House",
                        "acronym": "ED",
                        "phone": "(360) 786-7100"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetActiveCommittees",
                "count": 1
            }
        }
    """
    try:
        logger.info("Fetching all active committees")

        # Call WSLClient to get active committees
        committees_data = wsl_client.get_active_committees()

        # Handle case where no committees exist
        if not committees_data or len(committees_data) == 0:
            return {
                "success": True,
                "data": {"committees": []},
                "metadata": {
                    "message": "No active committees found",
                    "api_call": "GetActiveCommittees",
                    "count": 0,
                },
            }

        # Format committee data
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
            "success": True,
            "data": {"committees": formatted_committees},
            "metadata": {
                "api_call": "GetActiveCommittees",
                "count": len(formatted_committees),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching active committees: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch active committees: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_active_committees",
                "api_call": "GetActiveCommittees",
            },
        }



def get_active_house_committees() -> Dict[str, Any]:
    """
    Retrieve all currently active House committees.

    This tool fetches active committees from the House of Representatives,
    including committee names, acronyms, phone numbers, and agency information.

    Returns:
        Dict containing list of active House committees with metadata.
        Returns empty list with descriptive message if no committees exist.

    Example:
        >>> get_active_house_committees()
        {
            "success": True,
            "data": {
                "committees": [
                    {
                        "id": "123",
                        "name": "Education",
                        "long_name": "House Committee on Education",
                        "agency": "House",
                        "acronym": "ED",
                        "phone": "(360) 786-7100"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetActiveHouseCommittees",
                "count": 1
            }
        }
    """
    try:
        logger.info("Fetching active House committees")

        # Call WSLClient to get active House committees
        committees_data = wsl_client.get_active_house_committees()

        # Handle case where no committees exist
        if not committees_data or len(committees_data) == 0:
            return {
                "success": True,
                "data": {"committees": []},
                "metadata": {
                    "message": "No active House committees found",
                    "api_call": "GetActiveHouseCommittees",
                    "count": 0,
                },
            }

        # Format committee data
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
            "success": True,
            "data": {"committees": formatted_committees},
            "metadata": {
                "api_call": "GetActiveHouseCommittees",
                "count": len(formatted_committees),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching active House committees: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch active House committees: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_active_house_committees",
                "api_call": "GetActiveHouseCommittees",
            },
        }


def get_active_senate_committees() -> Dict[str, Any]:
    """
    Retrieve all currently active Senate committees.

    This tool fetches active committees from the Senate,
    including committee names, acronyms, phone numbers, and agency information.

    Returns:
        Dict containing list of active Senate committees with metadata.
        Returns empty list with descriptive message if no committees exist.

    Example:
        >>> get_active_senate_committees()
        {
            "success": True,
            "data": {
                "committees": [
                    {
                        "id": "456",
                        "name": "Ways & Means",
                        "long_name": "Senate Committee on Ways & Means",
                        "agency": "Senate",
                        "acronym": "WM",
                        "phone": "(360) 786-7715"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetActiveSenateCommittees",
                "count": 1
            }
        }
    """
    try:
        logger.info("Fetching active Senate committees")

        # Call WSLClient to get active Senate committees
        committees_data = wsl_client.get_active_senate_committees()

        # Handle case where no committees exist
        if not committees_data or len(committees_data) == 0:
            return {
                "success": True,
                "data": {"committees": []},
                "metadata": {
                    "message": "No active Senate committees found",
                    "api_call": "GetActiveSenateCommittees",
                    "count": 0,
                },
            }

        # Format committee data
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
            "success": True,
            "data": {"committees": formatted_committees},
            "metadata": {
                "api_call": "GetActiveSenateCommittees",
                "count": len(formatted_committees),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching active Senate committees: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch active Senate committees: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_active_senate_committees",
                "api_call": "GetActiveSenateCommittees",
            },
        }


def get_active_committee_members(committee_name: str, agency: str) -> Dict[str, Any]:
    """
    Retrieve members of an active committee.

    This tool fetches current committee membership including member names,
    roles (chair/vice-chair/member), party affiliation, district, and contact information.

    Args:
        committee_name: Name of the committee (e.g., "Education", "Ways & Means")
        agency: Chamber - "House" or "Senate"

    Returns:
        Dict containing list of committee members with metadata.
        Returns empty list with descriptive message if no members exist.

    Example:
        >>> get_active_committee_members("Education", "House")
        {
            "success": True,
            "data": {
                "committee_name": "Education",
                "agency": "House",
                "members": [
                    {
                        "id": "789",
                        "name": "John Doe",
                        "party": "D",
                        "district": "43",
                        "role": "Chair",
                        "phone": "(360) 786-7100",
                        "email": "john.doe@leg.wa.gov"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetActiveCommitteeMembers",
                "count": 1
            }
        }
    """
    try:
        logger.info(f"Fetching active members for {agency} committee: {committee_name}")

        # Call WSLClient to get active committee members
        members_data = wsl_client.get_active_committee_members(agency, committee_name)

        # Handle case where no members exist
        if not members_data or len(members_data) == 0:
            return {
                "success": True,
                "data": {
                    "committee_name": committee_name,
                    "agency": agency,
                    "members": [],
                },
                "metadata": {
                    "message": f"No active members found for {agency} committee: {committee_name}",
                    "api_call": "GetActiveCommitteeMembers",
                    "count": 0,
                },
            }

        # Format member data
        formatted_members = []
        for member in members_data:
            formatted_members.append(
                {
                    "id": member.get("id", ""),
                    "name": member.get("name", ""),
                    "party": member.get("party", ""),
                    "district": member.get("district", ""),
                    "role": member.get("role", ""),
                    "phone": member.get("phone", ""),
                    "email": member.get("email", ""),
                }
            )

        return {
            "success": True,
            "data": {
                "committee_name": committee_name,
                "agency": agency,
                "members": formatted_members,
            },
            "metadata": {
                "api_call": "GetActiveCommitteeMembers",
                "count": len(formatted_members),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching active committee members: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch active committee members: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_active_committee_members",
                "api_call": "GetActiveCommitteeMembers",
            },
        }


def get_committee_members(committee_name: str, agency: str, biennium: str = None) -> Dict[str, Any]:
    """
    Retrieve committee members for a specific biennium (historical composition).

    This tool fetches historical committee membership including member names,
    roles (chair/vice-chair/member), party affiliation, district, and contact information.

    Args:
        committee_name: Name of the committee (e.g., "Education", "Ways & Means")
        agency: Chamber - "House" or "Senate"
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of committee members with metadata.
        Returns empty list with descriptive message if no members exist.

    Example:
        >>> get_committee_members("Education", "House", "2023-24")
        {
            "success": True,
            "data": {
                "committee_name": "Education",
                "agency": "House",
                "biennium": "2023-24",
                "members": [
                    {
                        "id": "789",
                        "name": "John Doe",
                        "party": "D",
                        "district": "43",
                        "role": "Chair",
                        "phone": "(360) 786-7100",
                        "email": "john.doe@leg.wa.gov"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetCommitteeMembers",
                "count": 1
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching members for {agency} committee: {committee_name} in biennium {biennium}")

        # Call WSLClient to get committee members
        members_data = wsl_client.get_committee_members(biennium, agency, committee_name)

        # Handle case where no members exist
        if not members_data or len(members_data) == 0:
            return {
                "success": True,
                "data": {
                    "committee_name": committee_name,
                    "agency": agency,
                    "biennium": biennium,
                    "members": [],
                },
                "metadata": {
                    "message": f"No members found for {agency} committee: {committee_name} in biennium {biennium}",
                    "api_call": "GetCommitteeMembers",
                    "count": 0,
                },
            }

        # Format member data
        formatted_members = []
        for member in members_data:
            formatted_members.append(
                {
                    "id": member.get("id", ""),
                    "name": member.get("name", ""),
                    "party": member.get("party", ""),
                    "district": member.get("district", ""),
                    "role": member.get("role", ""),
                    "phone": member.get("phone", ""),
                    "email": member.get("email", ""),
                }
            )

        return {
            "success": True,
            "data": {
                "committee_name": committee_name,
                "agency": agency,
                "biennium": biennium,
                "members": formatted_members,
            },
            "metadata": {
                "api_call": "GetCommitteeMembers",
                "count": len(formatted_members),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching committee members: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch committee members: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_committee_members",
                "api_call": "GetCommitteeMembers",
            },
        }


def get_house_committees(biennium: str = None) -> Dict[str, Any]:
    """
    Retrieve all House committees for a specific biennium.

    This tool fetches all House committees for a given biennium,
    including committee names, acronyms, phone numbers, and agency information.

    Args:
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of House committees with metadata.
        Returns empty list with descriptive message if no committees exist.

    Example:
        >>> get_house_committees("2023-24")
        {
            "success": True,
            "data": {
                "biennium": "2023-24",
                "committees": [
                    {
                        "id": "123",
                        "name": "Education",
                        "long_name": "House Committee on Education",
                        "agency": "House",
                        "acronym": "ED",
                        "phone": "(360) 786-7100"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetHouseCommittees",
                "count": 1
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching House committees for biennium {biennium}")

        # Call WSLClient to get House committees
        committees_data = wsl_client.get_house_committees(biennium)

        # Handle case where no committees exist
        if not committees_data or len(committees_data) == 0:
            return {
                "success": True,
                "data": {"biennium": biennium, "committees": []},
                "metadata": {
                    "message": f"No House committees found for biennium {biennium}",
                    "api_call": "GetHouseCommittees",
                    "count": 0,
                },
            }

        # Format committee data
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
            "success": True,
            "data": {"biennium": biennium, "committees": formatted_committees},
            "metadata": {
                "api_call": "GetHouseCommittees",
                "count": len(formatted_committees),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching House committees: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch House committees: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_house_committees",
                "api_call": "GetHouseCommittees",
            },
        }


def get_senate_committees(biennium: str = None) -> Dict[str, Any]:
    """
    Retrieve all Senate committees for a specific biennium.

    This tool fetches all Senate committees for a given biennium,
    including committee names, acronyms, phone numbers, and agency information.

    Args:
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing list of Senate committees with metadata.
        Returns empty list with descriptive message if no committees exist.

    Example:
        >>> get_senate_committees("2023-24")
        {
            "success": True,
            "data": {
                "biennium": "2023-24",
                "committees": [
                    {
                        "id": "456",
                        "name": "Ways & Means",
                        "long_name": "Senate Committee on Ways & Means",
                        "agency": "Senate",
                        "acronym": "WM",
                        "phone": "(360) 786-7715"
                    }
                ]
            },
            "metadata": {
                "api_call": "GetSenateCommittees",
                "count": 1
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        logger.info(f"Fetching Senate committees for biennium {biennium}")

        # Call WSLClient to get Senate committees
        committees_data = wsl_client.get_senate_committees(biennium)

        # Handle case where no committees exist
        if not committees_data or len(committees_data) == 0:
            return {
                "success": True,
                "data": {"biennium": biennium, "committees": []},
                "metadata": {
                    "message": f"No Senate committees found for biennium {biennium}",
                    "api_call": "GetSenateCommittees",
                    "count": 0,
                },
            }

        # Format committee data
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
            "success": True,
            "data": {"biennium": biennium, "committees": formatted_committees},
            "metadata": {
                "api_call": "GetSenateCommittees",
                "count": len(formatted_committees),
            },
        }

    except Exception as e:
        logger.error(f"Error fetching Senate committees: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch Senate committees: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_senate_committees",
                "api_call": "GetSenateCommittees",
            },
        }
