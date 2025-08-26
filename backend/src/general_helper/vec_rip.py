"""
Vector removal utility for resume data
Removes vector data from resume dictionaries to reduce payload size for frontend
"""

import copy
from typing import Dict, Any, List, Union


def vec_rip(
    data: Union[Dict[str, Any], List[Dict[str, Any]]]
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Recursively removes vector data from resume dictionary responses.
    This function removes 'vec' fields from 'aux_info' dictionaries throughout
    the nested structure to reduce payload size when sending to frontend.

    Args:
        data: Dictionary or list of dictionaries containing resume data with vectors

    Returns:
        Clean dictionary/list with all vector data removed

    Example:
        # Single dictionary
        clean_data = vec_rip(table_1[0])

        # List of dictionaries
        clean_data = vec_rip(table_1)
    """
    if data is None:
        return data

    # Handle list of dictionaries
    if isinstance(data, list):
        return [vec_rip(item) for item in data]

    # Handle single dictionary
    if isinstance(data, dict):
        # Create a deep copy to avoid modifying the original
        clean_data = copy.deepcopy(data)

        # Recursively process the dictionary
        _remove_vectors_recursive(clean_data)

        return clean_data

    # Return unchanged for non-dict, non-list types
    return data


def _remove_vectors_recursive(obj: Any) -> None:
    """
    Helper function to recursively remove vectors from nested structures.
    Modifies the object in place.

    Args:
        obj: Object to process (dict, list, or other)
    """
    if isinstance(obj, dict):
        # Remove 'vec' from 'aux_info' if it exists
        if "aux_info" in obj and isinstance(obj["aux_info"], dict):
            if "vec" in obj["aux_info"]:
                del obj["aux_info"]["vec"]

        # Recursively process all values in the dictionary
        for value in obj.values():
            _remove_vectors_recursive(value)

    elif isinstance(obj, list):
        # Recursively process all items in the list
        for item in obj:
            _remove_vectors_recursive(item)
