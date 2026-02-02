"""
RCW citation-related MCP tools for Washington State Legislature data.
"""

import logging
from typing import Any, Dict, Optional

from ..clients.wsl_client import WSLClient
from ..utils.formatters import get_current_biennium

logger = logging.getLogger(__name__)

wsl_client = WSLClient()


def get_rcw_cites_affected(bill_number: str, biennium: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve RCW sections affected by a specific bill.

    This tool fetches all Revised Code of Washington (RCW) sections that are
    affected by a bill, including the action type (amended, repealed, created)
    and formatted in standard RCW notation.

    Args:
        bill_number: Bill number in format "HB 1234" or "SB 5678" or just the number (e.g., "1234")
        biennium: Legislative biennium in format "YYYY-YY" (e.g., "2023-24") (optional, defaults to current)

    Returns:
        Dict containing RCW citations organized by action type.
        Returns empty list with descriptive message if no RCW sections are affected.

    Example:
        >>> get_rcw_cites_affected("HB 1234", "2023-24")
        {
            "success": True,
            "data": {
                "bill_number": "HB 1234",
                "bill_id": "HB 1234",
                "biennium": "2023-24",
                "rcw_citations": {
                    "amended": [
                        {
                            "citation": "RCW 28A.150.260",
                            "chapter": "28A.150",
                            "section": "260",
                            "action": "Amended"
                        }
                    ],
                    "repealed": [],
                    "created": []
                },
                "total_count": 1
            },
            "metadata": {
                "api_call": "GetRcwCitesAffected",
                "count": 1
            }
        }
    """
    try:
        # Use current biennium if none provided
        if not biennium:
            biennium = get_current_biennium()

        # Parse bill number to determine bill ID format
        bill_num_str = bill_number.strip()
        
        # Determine bill ID format (need "HB 1234" or "SB 5678" format)
        if " " in bill_num_str:
            # Already in correct format
            bill_id = bill_num_str
        else:
            # Just a number - we need to determine chamber
            # For now, we'll try both and see which works
            # This is a limitation of the API - it requires the full bill ID
            return {
                "success": False,
                "error": f"Bill number must include chamber prefix (e.g., 'HB 1234' or 'SB 5678'). Got: {bill_number}",
                "error_type": "validation",
                "metadata": {
                    "tool_name": "get_rcw_cites_affected",
                    "api_call": "GetRcwCitesAffected",
                },
            }

        logger.info(f"Fetching RCW citations for bill {bill_id} in biennium {biennium}")

        # Call WSLClient to get RCW citation data
        rcw_data = wsl_client.get_rcw_cites_affected(biennium, bill_id)

        # Handle case where no RCW citations exist
        if not rcw_data or len(rcw_data) == 0:
            return {
                "success": True,
                "data": {
                    "bill_number": bill_number,
                    "bill_id": bill_id,
                    "biennium": biennium,
                    "rcw_citations": {
                        "amended": [],
                        "repealed": [],
                        "created": [],
                    },
                    "total_count": 0,
                },
                "metadata": {
                    "message": f"No RCW citations found for bill {bill_number} in biennium {biennium}",
                    "api_call": "GetRcwCitesAffected",
                },
            }

        # Parse and format RCW citation data, organized by action type
        citations_by_action = {
            "amended": [],
            "repealed": [],
            "created": [],
        }

        for citation in rcw_data:
            # Format RCW citation in standard notation (e.g., "RCW 28A.150.260")
            chapter = citation.get("rcw_chapter", "")
            section = citation.get("rcw_section", "")
            
            # Build standard RCW notation
            if chapter and section:
                formatted_citation = f"RCW {chapter}.{section}"
            elif chapter:
                formatted_citation = f"RCW {chapter}"
            else:
                formatted_citation = "RCW (unknown)"

            action = citation.get("action", "").lower()
            
            citation_entry = {
                "citation": formatted_citation,
                "chapter": chapter,
                "section": section,
                "action": citation.get("action", ""),
            }

            # Organize by action type
            if "amend" in action:
                citations_by_action["amended"].append(citation_entry)
            elif "repeal" in action:
                citations_by_action["repealed"].append(citation_entry)
            elif "create" in action or "new" in action or "add" in action:
                citations_by_action["created"].append(citation_entry)
            else:
                # Default to amended if action type is unclear
                citations_by_action["amended"].append(citation_entry)

        total_count = sum(len(v) for v in citations_by_action.values())

        return {
            "success": True,
            "data": {
                "bill_number": bill_number,
                "bill_id": bill_id,
                "biennium": biennium,
                "rcw_citations": citations_by_action,
                "total_count": total_count,
            },
            "metadata": {"api_call": "GetRcwCitesAffected", "count": total_count},
        }

    except Exception as e:
        logger.error(f"Error fetching RCW citations for bill {bill_number}: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch RCW citations: {str(e)}",
            "error_type": "unexpected",
            "metadata": {
                "tool_name": "get_rcw_cites_affected",
                "api_call": "GetRcwCitesAffected",
            },
        }
