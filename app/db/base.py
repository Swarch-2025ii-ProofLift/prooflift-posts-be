"""
Database base configuration.
"""

from typing import Any

def get_db() -> Any:
    """Return a database connection/session."""
    raise NotImplementedError("Implement DB session/connection here")
