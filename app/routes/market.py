"""Regional market demand routes."""

from fastapi import APIRouter, Depends, status
from app.schemas.market import MarketDemandRequest, MarketDemandResponse
from app.services.market.demand import BaseMarketDemandService, MarketDemandService

router = APIRouter(prefix="/market", tags=["Market Intelligence"])


def get_market_service() -> BaseMarketDemandService:
    return MarketDemandService()


@router.post(
    "/demand",
    response_model=MarketDemandResponse,
    status_code=status.HTTP_200_OK,
    summary="Fetch regional and district skill market demand trends",
)
async def get_market_demand(
    request: MarketDemandRequest,
    service: BaseMarketDemandService = Depends(get_market_service),
) -> MarketDemandResponse:
    """Analyze and return district-level labor market demand."""
    return await service.analyze_demand(request)
