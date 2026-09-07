"""
Market Demand Service Interface and Placeholder.
Analyzes regional/district labor market trends and high-demand skill areas.
"""

from abc import ABC, abstractmethod
from app.core.exceptions import ServiceNotImplementedException
from app.schemas.market import MarketDemandRequest, MarketDemandResponse


class BaseMarketDemandService(ABC):
    """Abstract base interface for regional labor demand analysis."""

    @abstractmethod
    async def analyze_demand(self, request: MarketDemandRequest) -> MarketDemandResponse:
        """Fetch and analyze local market skill demand."""
        pass


class MarketDemandService(BaseMarketDemandService):
    """Production service placeholder for market demand."""

    async def analyze_demand(self, request: MarketDemandRequest) -> MarketDemandResponse:
        raise ServiceNotImplementedException(
            service_name="MarketDemandService.analyze_demand",
            details={"state": request.state, "district": request.district},
        )
