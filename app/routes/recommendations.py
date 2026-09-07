"""NSQF recommendation routes."""

from fastapi import APIRouter, Depends, status
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.services.recommendation.recommender import (
    BaseRecommendationService,
    RecommendationService,
)

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


def get_recommendation_service() -> BaseRecommendationService:
    return RecommendationService()


@router.post(
    "",
    response_model=RecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate NSQF-aligned skilling and livelihood recommendations",
)
async def generate_recommendations(
    request: RecommendationRequest,
    service: BaseRecommendationService = Depends(get_recommendation_service),
) -> RecommendationResponse:
    """Generate recommendations based on candidate profile."""
    return await service.get_recommendations(request)
