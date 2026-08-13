"""Convert numpy values inside nested structures so they can be JSON-encoded."""

from typing import Any

try:  # numpy is present in every install, but keep the helper usable without it
    import numpy as np
except ImportError:  # pragma: no cover
    np = None


def json_safe(obj: Any) -> Any:
    """Recursively replace numpy arrays/scalars with plain Python values."""
    if np is not None:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.generic):
            return obj.item()
    if isinstance(obj, dict):
        return {key: json_safe(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(value) for value in obj]
    return obj
