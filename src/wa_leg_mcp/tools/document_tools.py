"""
Document Management Tools

MCP tools for retrieving legislative documents and document metadata.
"""

import logging
from typing import Any, Dict

from ..clients.wsl_client import WSLClient

logger = logging.getLogger(__name__)


def get_document_classes(biennium: str) -> Dict[str, Any]:
    """
    Get available document types for a biennium.

    Args:
        biennium: Biennium in format "2023-24"

    Returns:
        Dict with document class list including names and descriptions
    """
    try:
        client = WSLClient()
        result = client.get_document_classes(biennium)

        if result is None:
            return {
                "success": False,
                "error": f"Failed to retrieve document classes for biennium {biennium}",
            }

        if not result:
            return {
                "success": True,
                "data": [],
                "metadata": {
                    "message": f"No document classes found for biennium {biennium}",
                    "biennium": biennium,
                },
            }

        return {
            "success": True,
            "data": result,
            "metadata": {
                "count": len(result),
                "biennium": biennium,
            },
        }

    except Exception as e:
        logger.error(f"Error getting document classes for {biennium}: {e}", exc_info=True)
        return {
            "success": False,
            "error": f"An error occurred while retrieving document classes: {str(e)}",
        }


def get_all_documents_by_class(biennium: str, document_class: str) -> Dict[str, Any]:
    """
    Get all documents of a specific class.

    Args:
        biennium: Biennium in format "2023-24"
        document_class: Document class (e.g., "Bills", "Amendments")

    Returns:
        Dict with document list including names, URLs, bill associations
    """
    try:
        client = WSLClient()
        result = client.get_all_documents_by_class(biennium, document_class)

        if result is None:
            return {
                "success": False,
                "error": f"Failed to retrieve documents for class '{document_class}' in biennium {biennium}",
            }

        if not result:
            return {
                "success": True,
                "data": [],
                "metadata": {
                    "message": f"No documents found for class '{document_class}' in biennium {biennium}",
                    "biennium": biennium,
                    "document_class": document_class,
                },
            }

        return {
            "success": True,
            "data": result,
            "metadata": {
                "count": len(result),
                "biennium": biennium,
                "document_class": document_class,
            },
        }

    except Exception as e:
        logger.error(
            f"Error getting documents for class '{document_class}' in {biennium}: {e}",
            exc_info=True,
        )
        return {
            "success": False,
            "error": f"An error occurred while retrieving documents: {str(e)}",
        }


def get_documents_by_class(
    biennium: str, document_class: str, name_filter: str
) -> Dict[str, Any]:
    """
    Get documents by class with name filter.

    Args:
        biennium: Biennium in format "2023-24"
        document_class: Document class (e.g., "Bills")
        name_filter: Pattern to match (e.g., "HB 1*")

    Returns:
        Dict with filtered document list
    """
    try:
        client = WSLClient()
        result = client.get_documents_by_class(biennium, document_class, name_filter)

        if result is None:
            return {
                "success": False,
                "error": f"Failed to retrieve documents for class '{document_class}' with filter '{name_filter}' in biennium {biennium}",
            }

        if not result:
            return {
                "success": True,
                "data": [],
                "metadata": {
                    "message": f"No documents found for class '{document_class}' matching filter '{name_filter}' in biennium {biennium}",
                    "biennium": biennium,
                    "document_class": document_class,
                    "name_filter": name_filter,
                },
            }

        return {
            "success": True,
            "data": result,
            "metadata": {
                "count": len(result),
                "biennium": biennium,
                "document_class": document_class,
                "name_filter": name_filter,
            },
        }

    except Exception as e:
        logger.error(
            f"Error getting documents for class '{document_class}' with filter '{name_filter}' in {biennium}: {e}",
            exc_info=True,
        )
        return {
            "success": False,
            "error": f"An error occurred while retrieving documents: {str(e)}",
        }
