"""Personalized skilling and livelihood progression roadmap schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.profile import CandidateProfile
from app.schemas.recommendation import QualificationPack


class RoadmapMilestone(BaseModel):
    step_number: int
    title: str
    description: str
    estimated_duration_weeks: int
    prerequisites: List[str] = Field(default_factory=list)
    action_items: List[str] = Field(default_factory=list)
    support_schemes: List[str] = Field(default_factory=list, description="Relevant PM-AJAY or allied subsidies")


class RoadmapRequest(BaseModel):
    profile: CandidateProfile
    target_role: QualificationPack
    timeframe_months: Optional[int] = Field(default=6, ge=1, le=24)


class RoadmapResponse(BaseModel):
    candidate_id: Optional[str] = None
    target_role_title: str
    total_estimated_weeks: int = 0
    milestones: List[RoadmapMilestone] = Field(default_factory=list)
    status: str = Field(default="pending_ai_implementation")
