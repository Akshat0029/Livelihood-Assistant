"""Personalized career and skilling roadmap routes."""

from fastapi import APIRouter, Depends, status
from app.schemas.roadmap import RoadmapRequest, RoadmapResponse
from app.services.roadmap.generator import BaseRoadmapService, RoadmapService

router = APIRouter(prefix="/roadmap", tags=["Career Roadmap"])


def get_roadmap_service() -> BaseRoadmapService:
    return RoadmapService()


@router.post(
    "",
    response_model=RoadmapResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate personalized skilling & livelihood progression roadmap",
)
async def generate_career_roadmap(
    request: RoadmapRequest,
    service: BaseRoadmapService = Depends(get_roadmap_service),
) -> RoadmapResponse:
    """Generate structured step-by-step roadmap towards target NSQF role."""
    return await service.generate_roadmap(request)
