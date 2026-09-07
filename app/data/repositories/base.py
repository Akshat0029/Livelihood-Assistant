"""
Base repository interface.
Defines clean storage and lookup contracts without direct database dependencies.
"""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Generic base repository for in-memory or localized file storage."""

    @abstractmethod
    def get_by_id(self, item_id: str) -> Optional[T]:
        """Fetch entity by unique identifier."""
        pass

    @abstractmethod
    def list_all(self) -> List[T]:
        """List all entities."""
        pass

    @abstractmethod
    def add(self, item: T) -> T:
        """Add new entity."""
        pass
