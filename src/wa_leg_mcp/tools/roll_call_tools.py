"""
Roll call and voting-related MCP tools for Washington State Legislature data.
"""

import logging
from typing import Any, Dict, Optional

from ..clients.wsl_client import WSLClient
from ..utils.formatters import get_current_biennium

logger = logging.getLogger(__name__)

wsl_client = WSLClient()


def get_roll_calls(bill_number: str, biennium: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve roll call votes for a specific bill.

    This tool fetches all roll call voting records for a bill, including how each
    legislator voted (yea, nay, absent, excused), vote dates, and vote descriptions.

    Args:
        bill_number: Bill number in format "HB 1234" or "SB 5678" or just the number (e.g., "1234")
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing roll call votes with legislator names, vote values, and dates.
        Returns empty list with descriptive message if no roll calls exist.

    Example:
        >>> get_roll_calls("HB 1234", "2023-24")
        {
            "success": True,
            "data": {
                "bill_number": "HB 1234",
                "biennium": "2023-24",
                "roll_calls": [
                    {
                        "sequence_number": 1,
                        "date": "2023-03-15",
                        "description": "Final Passage",
                        "yea_votes": 65,
                        "nay_votes": 33,
                        "absent_votes": 0,
                        "excused_votes": 0,
                        "votes": [
                            {
                                "legislator_name": "Smith, John",
                                "vote": "Yea",
                                "district": "1",
                                "party": "D"
                            },
                            ...
                        ]
                    }
                ]
            },
            "metadata": {
                "api_call": "GetRollCalls",
                "timestamp": "2024-01-15T10:30:00Z"
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
                    "tool_name": "get_roll_calls",
                    "api_call": "GetRollCalls"
                }
            }

        bill_num = int(bill_num_str)

        logger.info(f"Fetching roll calls for bill {bill_num} in biennium {biennium}")

        # Call WSLClient to get roll call data
        roll_calls_data = wsl_client.get_roll_calls(biennium, bill_num)

        # Handle case where no roll calls exist
        if not roll_calls_data or len(roll_calls_data) == 0:
            return {
                "success": True,
                "data": {
                    "bill_number": bill_number,
                    "biennium": biennium,
                    "roll_calls": []
                },
                "metadata": {
                    "message": f"No roll calls found for bill {bill_number} in biennium {biennium}",
                    "api_call": "GetRollCalls"
                }
            }

        # Parse and format roll call data
        formatted_roll_calls = []
        
        for roll_call in roll_calls_data:
            # Extract vote counts
            yea_count = roll_call.get("yea_count", 0)
            nay_count = roll_call.get("nay_count", 0)
            absent_count = roll_call.get("absent_count", 0)
            excused_count = roll_call.get("excused_count", 0)
            
            # Extract individual votes
            votes_list = []
            votes_data = roll_call.get("votes", {})
            
            # The votes might be in an array_of_vote structure
            if isinstance(votes_data, dict):
                votes_array = votes_data.get("array_of_vote", [])
            elif isinstance(votes_data, list):
                votes_array = votes_data
            else:
                votes_array = []
            
            for vote in votes_array:
                votes_list.append({
                    "legislator_name": vote.get("name", ""),
                    "vote": vote.get("vote_value", ""),
                    "district": str(vote.get("district", "")),
                    "party": vote.get("party", "")
                })
            
            formatted_roll_calls.append({
                "sequence_number": roll_call.get("sequence_number", 0),
                "date": roll_call.get("vote_date", ""),
                "description": roll_call.get("motion", ""),
                "yea_votes": yea_count,
                "nay_votes": nay_count,
                "absent_votes": absent_count,
                "excused_votes": excused_count,
                "votes": votes_list
            })

        # Sort roll calls by sequence number (chronological order)
        formatted_roll_calls.sort(key=lambda x: x.get("sequence_number", 0))

        return {
            "success": True,
            "data": {
                "bill_number": bill_number,
                "biennium": biennium,
                "roll_calls": formatted_roll_calls
            },
            "metadata": {
                "api_call": "GetRollCalls",
                "count": len(formatted_roll_calls)
            }
        }

    except ValueError as e:
        logger.error(f"Invalid bill number format: {bill_number}")
        return {
            "success": False,
            "error": f"Invalid bill number: {bill_number}. Must be a valid number.",
            "error_type": "validation",
            "metadata": {
                "tool_name": "get_roll_calls",
                "api_call": "GetRollCalls"
            }
        }
    except Exception as e:
        logger.error(f"Error fetching roll calls for bill {bill_number}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch roll calls: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_roll_calls",
                "api_call": "GetRollCalls"
            }
        }
