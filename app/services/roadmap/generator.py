"""
Roadmap Service Interface and Placeholder.
Generates milestone-driven career progression and skilling pathways aligned with PM-AJAY.
"""

from abc import ABC, abstractmethod
from app.core.exceptions import ServiceNotImplementedException
from app.schemas.roadmap import RoadmapRequest, RoadmapResponse


class BaseRoadmapService(ABC):
    """Abstract base interface for roadmap generation."""

    @abstractmethod
    async def generate_roadmap(self, request: RoadmapRequest) -> RoadmapResponse:
        """Generate structured roadmap for candidate to achieve target qualification pack."""
        pass


class RoadmapService(BaseRoadmapService):
    """Production service placeholder for roadmap generation."""

    async def generate_roadmap(self, request: RoadmapRequest) -> RoadmapResponse:
        raise ServiceNotImplementedException(
            service_name="RoadmapService.generate_roadmap",
            details={
                "candidate_id": request.profile.candidate_id,
                "target_role": request.target_role.job_role,
            },
        )
