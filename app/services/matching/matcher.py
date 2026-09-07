"""
Skill Matching Service Interface and Placeholder.
Matches candidate existing skills and experience to NSQF qualification packs and competencies.
"""

from abc import ABC, abstractmethod
from typing import List
from app.core.exceptions import ServiceNotImplementedException
from app.schemas.profile import CandidateProfile
from app.schemas.recommendation import QualificationPack, SkillingRecommendation


class BaseSkillMatchingService(ABC):
    """Abstract base interface for matching candidate skills to NSQF packs."""

    @abstractmethod
    async def match_skills(
        self, profile: CandidateProfile, target_packs: List[QualificationPack]
    ) -> List[SkillingRecommendation]:
        """Perform semantic matching between candidate skills and qualification packs."""
        pass


class SkillMatchingService(BaseSkillMatchingService):
    """Production service placeholder for skill matching."""

    async def match_skills(
        self, profile: CandidateProfile, target_packs: List[QualificationPack]
    ) -> List[SkillingRecommendation]:
        raise ServiceNotImplementedException(
            service_name="SkillMatchingService.match_skills",
            details={"candidate_id": profile.candidate_id, "num_target_packs": len(target_packs)},
        )
