"""Schemas module index exporting API request/response models."""

from app.schemas.common import APIResponse, ErrorDetail, ServiceStatus
from app.schemas.health import HealthResponse
from app.schemas.profile import (
    CandidateProfile,
    Demographics,
    EducationHistory,
    WorkExperience,
    ProfileExtractRequest,
    ProfileExtractResponse,
    ProfileValidateRequest,
    ProfileValidateResponse,
    EligibilityCheck,
)
from app.schemas.recommendation import (
    QualificationPack,
    SkillingRecommendation,
    RecommendationRequest,
    RecommendationResponse,
)
from app.schemas.speech import (
    SpeechTranscribeRequest,
    SpeechTranscribeResponse,
)
from app.schemas.opportunity import (
    ParsedOpportunity,
    OpportunityParseRequest,
    OpportunityParseResponse,
)
from app.schemas.market import (
    SectorDemand,
    MarketDemandRequest,
    MarketDemandResponse,
)
from app.schemas.roadmap import (
    RoadmapMilestone,
    RoadmapRequest,
    RoadmapResponse,
)

__all__ = [
    "APIResponse",
    "ErrorDetail",
    "ServiceStatus",
    "HealthResponse",
    "CandidateProfile",
    "Demographics",
    "EducationHistory",
    "WorkExperience",
    "ProfileExtractRequest",
    "ProfileExtractResponse",
    "ProfileValidateRequest",
    "ProfileValidateResponse",
    "EligibilityCheck",
    "QualificationPack",
    "SkillingRecommendation",
    "RecommendationRequest",
    "RecommendationResponse",
    "SpeechTranscribeRequest",
    "SpeechTranscribeResponse",
    "ParsedOpportunity",
    "OpportunityParseRequest",
    "OpportunityParseResponse",
    "SectorDemand",
    "MarketDemandRequest",
    "MarketDemandResponse",
    "RoadmapMilestone",
    "RoadmapRequest",
    "RoadmapResponse",
]
