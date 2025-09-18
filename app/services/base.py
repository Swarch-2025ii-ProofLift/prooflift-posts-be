"""
Base service class.
Services contain business logic and orchestrate repositories.
"""

from typing import Any

class BaseService:
    """Generic service with extendable methods."""

    def __init__(self, repo: Any):
        self.repo = repo
