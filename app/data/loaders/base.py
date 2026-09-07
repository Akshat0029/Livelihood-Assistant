"""
Base data loader interface.
Allows loading NSQF qualification packs, occupational standards, and regional market data
from local files or datasets without external database coupling.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List, Optional


class BaseDataLoader(ABC):
    """Abstract data loader for dataset ingestion."""

    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path

    @abstractmethod
    def load(self) -> List[Any]:
        """Load and parse source data."""
        pass
