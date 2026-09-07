"""Data layer package."""

from app.data.loaders.base import BaseDataLoader
from app.data.repositories.base import BaseRepository

__all__ = ["BaseDataLoader", "BaseRepository"]
