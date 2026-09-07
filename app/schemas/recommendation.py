"""NSQF-aligned skilling and livelihood recommendation schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.profile import CandidateProfile


class QualificationPack(BaseModel):
    qp_code: str = Field(..., description="NSQF Qualification Pack Code (e.g. ELE/Q0101)")
    job_role: str = Field(..., description="Job role name")
    nsqf_level: int = Field(..., ge=1, le=10, description="NSQF Level 1 to 10")
    sector: str = Field(..., description="Industry Sector Skill Council")
    training_duration_hours: Optional[int] = None
    expected_salary_range: Optional[str] = None


class SkillingRecommendation(BaseModel):
    qualification_pack: QualificationPack
    relevance_score: float = Field(default=0.0, ge=0.0, le=1.0)
    match_reasons: List[str] = Field(default_factory=list)
    skill_gap: List[str] = Field(default_factory=list)
    nearby_training_centers: List[str] = Field(default_factory=list)


class RecommendationRequest(BaseModel):
    profile: CandidateProfile
    target_sector: Optional[str] = None
    max_recommendations: int = Field(default=5, ge=1, le=20)
    location_filter: Optional[str] = None


class RecommendationResponse(BaseModel):
    candidate_id: Optional[str] = None
    recommendations: List[SkillingRecommendation] = Field(default_factory=list)
    total_found: int = 0
    status: str = Field(default="pending_ai_implementation")
