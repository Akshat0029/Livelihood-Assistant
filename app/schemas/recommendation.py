"""Canonical recommendation domain models supporting multi-pathway career suggestions."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.common import SourceEvidence
from app.schemas.course import NSQFCourse
from app.schemas.eligibility import EligibilityResult
from app.schemas.occupation import Occupation
from app.schemas.opportunity import Opportunity
from app.schemas.profile import BeneficiaryProfile
from app.schemas.skill import SkillGap


class PathwayType(str, Enum):
    SKILL_TRAINING = "skill_training"
    DIRECT_EMPLOYMENT = "direct_employment"
    ENTREPRENEURSHIP = "entrepreneurship"
    APPRENTICESHIP = "apprenticeship"
    COMBINED = "combined"


class ScoreBreakdown(BaseModel):
    """Detailed multidimensional scoring for a recommendation."""

    skill_match_score: float = Field(
        ..., ge=0.0, le=1.0, description="Semantic skill overlap index between 0.0 and 1.0"
    )
    local_demand_score: float = Field(
        ..., ge=0.0, le=1.0, description="District/regional labor demand signal index"
    )
    eligibility_score: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Scheme eligibility confidence"
    )
    preference_alignment_score: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Alignment with beneficiary goals"
    )


class Recommendation(BaseModel):
    """Canonical recommendation entity representing a validated skilling/career pathway."""

    recommendation_id: str = Field(..., description="Unique recommendation identifier")
    pathway_type: PathwayType = Field(..., description="Classification of recommended pathway")
    occupation_reference: Optional[str] = Field(
        default=None, description="Target canonical occupation ID or title"
    )
    target_occupation: Optional[Occupation] = Field(
        default=None, description="Detailed target occupation entity when available"
    )
    course_reference: Optional[str] = Field(
        default=None, description="Recommended NSQF course ID or QP code when applicable"
    )
    target_course: Optional[NSQFCourse] = Field(
        default=None, description="Detailed target NSQF course entity when available"
    )
    opportunity_references: List[str] = Field(
        default_factory=list,
        description="Associated local job, apprenticeship, or PM-AJAY opportunity IDs",
    )
    associated_opportunities: List[Opportunity] = Field(
        default_factory=list,
        description="Detailed opportunities when resolved",
    )
    overall_score: float = Field(
        ..., ge=0.0, le=1.0, description="Composite recommendation rank score [0.0, 1.0]"
    )
    score_breakdown: ScoreBreakdown = Field(
        ..., description="Granular scoring dimensions supporting transparency"
    )
    eligibility_result: Optional[EligibilityResult] = Field(
        default=None, description="Pre-computed eligibility check against scheme requirements"
    )
    matched_skills: List[str] = Field(
        default_factory=list, description="Skills beneficiary already possesses that apply"
    )
    skill_gaps: List[SkillGap] = Field(
        default_factory=list, description="Identified competency gaps with priority levels"
    )
    local_demand_signal: Optional[str] = Field(
        default=None, description="Qualitative summary of regional economic demand"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="System confidence score in this recommendation"
    )
    explanation: str = Field(
        ..., description="Plain-language justification presented to beneficiary"
    )
    model_version: str = Field(
        default="v1.0", description="Algorithm or ranking configuration version"
    )
    evidence: List[SourceEvidence] = Field(
        default_factory=list, description="Evidence references grounding this recommendation"
    )


class RecommendationRequest(BaseModel):
    profile: BeneficiaryProfile
    target_sector: Optional[str] = Field(
        default=None, description="Optional sector filter (e.g. Green Jobs, Electronics)"
    )
    preferred_pathway: Optional[PathwayType] = Field(
        default=None, description="Optional pathway preference filter"
    )
    max_recommendations: int = Field(
        default=5, ge=1, le=20, description="Maximum number of recommendations to return (e.g. Top 3-5)"
    )
    location_filter: Optional[str] = Field(
        default=None, description="Optional district/state restriction"
    )


class RecommendationResponse(BaseModel):
    candidate_id: Optional[str] = None
    recommendations: List[Recommendation] = Field(default_factory=list)
    total_found: int = 0
    status: str = Field(default="pending_ai_implementation")
