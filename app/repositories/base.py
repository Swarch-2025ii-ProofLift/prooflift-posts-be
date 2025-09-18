"""
Base repository class.
Repositories encapsulate DB access logic.
"""

from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")

class BaseRepository(Generic[T]):
    """Generic repository with common CRUD signatures."""

    def get(self, id: str) -> Optional[T]:
        raise NotImplementedError()

    def list(self) -> List[T]:
        raise NotImplementedError()

    def create(self, obj: T) -> T:
        raise NotImplementedError()

    def update(self, id: str, obj: T) -> T:
        raise NotImplementedError()

    def delete(self, id: str) -> None:
        raise NotImplementedError()
