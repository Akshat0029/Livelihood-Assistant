"""
NSQF-Aligned Recommendation Service Interface and Placeholder.
Recommends optimal skilling courses and PM-AJAY livelihood pathways.
"""

from abc import ABC, abstractmethod
from app.core.exceptions import ServiceNotImplementedException
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse


class BaseRecommendationService(ABC):
    """Abstract base interface for generating NSQF recommendations."""

    @abstractmethod
    async def get_recommendations(self, request: RecommendationRequest) -> RecommendationResponse:
        """Generate tailored NSQF skilling course and livelihood recommendations."""
        pass


class RecommendationService(BaseRecommendationService):
    """Production service placeholder for recommendations."""

    async def get_recommendations(self, request: RecommendationRequest) -> RecommendationResponse:
        raise ServiceNotImplementedException(
            service_name="RecommendationService.get_recommendations",
            details={
                "beneficiary_id": request.profile.beneficiary_id,
                "target_sector": request.target_sector,
            },
        )
