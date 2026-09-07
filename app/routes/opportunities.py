"""Opportunity parsing routes."""

from fastapi import APIRouter, Depends, status
from app.schemas.opportunity import OpportunityParseRequest, OpportunityParseResponse
from app.services.opportunity.parser import (
    BaseOpportunityParsingService,
    OpportunityParsingService,
)

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


def get_opportunity_service() -> BaseOpportunityParsingService:
    return OpportunityParsingService()


@router.post(
    "/parse",
    response_model=OpportunityParseResponse,
    status_code=status.HTTP_200_OK,
    summary="Parse opportunities from circulars, announcements, or scheme documents",
)
async def parse_opportunities(
    request: OpportunityParseRequest,
    service: BaseOpportunityParsingService = Depends(get_opportunity_service),
) -> OpportunityParseResponse:
    """Parse unstructured circular text into structured opportunities."""
    return await service.parse_opportunities(request)
