"""
Metadata and Reference Tools

MCP tools for retrieving legislative metadata and reference data.
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from ..clients.wsl_client import WSLClient

logger = logging.getLogger(__name__)

# Simple in-memory cache for legislation types
_legislation_types_cache: Optional[Dict[str, Any]] = None
_cache_timestamp: Optional[datetime] = None
CACHE_TTL_HOURS = 24


def get_legislation_types() -> Dict[str, Any]:
    """
    Get valid legislation types.

    This function implements 24-hour caching to improve performance.
    The cache is stored in memory and will be cleared on server restart.

    Returns:
        Dict with legislation type codes and descriptions
    """
    global _legislation_types_cache, _cache_timestamp

    try:
        # Check if cache is valid
        if _legislation_types_cache is not None and _cache_timestamp is not None:
            cache_age = datetime.now() - _cache_timestamp
            if cache_age < timedelta(hours=CACHE_TTL_HOURS):
                logger.info("Returning cached legislation types")
                return {
                    "success": True,
                    "data": _legislation_types_cache,
                    "metadata": {
                        "cached": True,
                        "cache_timestamp": _cache_timestamp.isoformat(),
                        "cache_age_seconds": int(cache_age.total_seconds()),
                    },
                }

        # Cache miss or expired - fetch from API
        client = WSLClient()
        result = client.get_legislation_types()

        if result is None:
            # API failure - return default set with warning if we have cached data
            if _legislation_types_cache is not None:
                logger.warning("API failed, returning stale cached data")
                return {
                    "success": True,
                    "data": _legislation_types_cache,
                    "metadata": {
                        "cached": True,
                        "stale": True,
                        "warning": "API unavailable, returning cached data",
                    },
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to retrieve legislation types and no cached data available",
                }

        if not result:
            return {
                "success": True,
                "data": [],
                "metadata": {
                    "message": "No legislation types found",
                    "cached": False,
                },
            }

        # Update cache
        _legislation_types_cache = result
        _cache_timestamp = datetime.now()

        return {
            "success": True,
            "data": result,
            "metadata": {
                "count": len(result),
                "cached": False,
                "cache_timestamp": _cache_timestamp.isoformat(),
            },
        }

    except Exception as e:
        logger.error(f"Error getting legislation types: {e}", exc_info=True)
        # Return cached data if available
        if _legislation_types_cache is not None:
            logger.warning("Exception occurred, returning cached data")
            return {
                "success": True,
                "data": _legislation_types_cache,
                "metadata": {
                    "cached": True,
                    "stale": True,
                    "warning": f"Error occurred: {str(e)}, returning cached data",
                },
            }
        return {
            "success": False,
            "error": f"An error occurred while retrieving legislation types: {str(e)}",
        }


def get_legislation_by_request_number(biennium: str, request_number: str) -> Dict[str, Any]:
    """
    Look up bill by original request number.

    Args:
        biennium: Biennium in format "2023-24"
        request_number: Request number (e.g., "23-1234")

    Returns:
        Dict with bill information or request status
    """
    try:
        # Validate request number format
        if not request_number or not isinstance(request_number, str):
            return {
                "success": False,
                "error": "Invalid request number format. Expected format: '23-1234'",
            }

        client = WSLClient()
        result = client.get_legislation_by_request_number(biennium, request_number)

        if result is None:
            return {
                "success": False,
                "error": f"Failed to retrieve legislation for request number {request_number} in biennium {biennium}",
            }

        if not result:
            return {
                "success": True,
                "data": {},
                "metadata": {
                    "message": f"No legislation found for request number {request_number} in biennium {biennium}. The request may be pending or invalid.",
                    "biennium": biennium,
                    "request_number": request_number,
                },
            }

        return {
            "success": True,
            "data": result,
            "metadata": {
                "biennium": biennium,
                "request_number": request_number,
            },
        }

    except Exception as e:
        logger.error(
            f"Error getting legislation by request number {request_number} in {biennium}: {e}",
            exc_info=True,
        )
        return {
            "success": False,
            "error": f"An error occurred while retrieving legislation: {str(e)}",
        }


def get_committee_meeting_items(meeting_id: int) -> Dict[str, Any]:
    """
    Get agenda items for a specific committee meeting.

    Args:
        meeting_id: Meeting identifier (agenda_id)

    Returns:
        Dict with agenda items including bills and topics
    """
    try:
        # Validate meeting_id
        if not isinstance(meeting_id, int) or meeting_id <= 0:
            return {
                "success": False,
                "error": "Invalid meeting ID. Expected a positive integer.",
            }

        client = WSLClient()
        result = client.get_committee_meeting_items(meeting_id)

        if result is None:
            return {
                "success": False,
                "error": f"Failed to retrieve meeting items for meeting ID {meeting_id}",
            }

        if not result:
            return {
                "success": True,
                "data": [],
                "metadata": {
                    "message": f"No agenda items found for meeting ID {meeting_id}",
                    "meeting_id": meeting_id,
                },
            }

        return {
            "success": True,
            "data": result,
            "metadata": {
                "count": len(result),
                "meeting_id": meeting_id,
            },
        }

    except Exception as e:
        logger.error(f"Error getting meeting items for meeting {meeting_id}: {e}", exc_info=True)
        return {
            "success": False,
            "error": f"An error occurred while retrieving meeting items: {str(e)}",
        }


def get_revised_committee_meetings(
    since_date: str, biennium: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get committee meetings revised since a date.

    Args:
        since_date: Date in ISO 8601 format (e.g., "2023-01-01")
        biennium: Optional biennium filter (e.g., "2023-24")

    Returns:
        Dict with revised meetings
    """
    try:
        # Validate date format
        try:
            datetime.fromisoformat(since_date)
        except ValueError:
            return {
                "success": False,
                "error": f"Invalid date format: {since_date}. Expected ISO 8601 format (e.g., '2023-01-01')",
            }

        client = WSLClient()
        result = client.get_revised_committee_meetings(since_date)

        if result is None:
            return {
                "success": False,
                "error": f"Failed to retrieve revised meetings since {since_date}",
            }

        # Filter by biennium if provided
        if biennium and result:
            result = [meeting for meeting in result if meeting.get("biennium") == biennium]

        if not result:
            message = f"No revised meetings found since {since_date}"
            if biennium:
                message += f" for biennium {biennium}"
            return {
                "success": True,
                "data": [],
                "metadata": {
                    "message": message,
                    "since_date": since_date,
                    "biennium": biennium,
                },
            }

        return {
            "success": True,
            "data": result,
            "metadata": {
                "count": len(result),
                "since_date": since_date,
                "biennium": biennium,
            },
        }

    except Exception as e:
        logger.error(f"Error getting revised meetings since {since_date}: {e}", exc_info=True)
        return {
            "success": False,
            "error": f"An error occurred while retrieving revised meetings: {str(e)}",
        }
