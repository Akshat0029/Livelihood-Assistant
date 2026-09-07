"""Schemas package index exporting all canonical domain models and API contracts."""

# Phase 3 — Ontology, Provenance, Location, Provider
from app.schemas.ontology import DataClassification, OntologyRecord
from app.schemas.provenance import DataSourceRecord, SourcePrecedence
from app.schemas.location import LocationRecord
from app.schemas.provider import AccreditationStatus, ProviderType, TrainingProvider

# Common & Metadata
from app.schemas.common import (
    APIResponse,
    EducationLevel,
    EmploymentPreference,
    ErrorDetail,
    Gender,
    GeographicLocation,
    ProfileSource,
    ServiceStatus,
    SourceEvidence,
    SourceType,
    VerificationStatus,
)

# Skills & Skill Gaps
from app.schemas.skill import (
    GapStatus,
    PriorityLevel,
    RawSkill,
    SkillNormalizationMethod,
    SkillNormalizationResult,
    SkillNormalizationStatus,
    Skill,
    SkillCategory,
    SkillGap,
    SkillProficiency,
    SkillSource,
)

# Occupations
from app.schemas.occupation import (
    EmploymentType,
    Occupation,
)

# NSQF Courses & Qualifications
from app.schemas.course import (
    NSQFCourse,
)

# Eligibility
from app.schemas.eligibility import (
    CriterionResult,
    EligibilityResult,
    EligibilityStatus,
)

# Beneficiary Profile
from app.schemas.profile import (
    BeneficiaryProfile,
    EducationEntry,
    ProfileExtractRequest,
    ProfileExtractResponse,
    ProfileValidateRequest,
    ProfileValidateResponse,
    WorkHistoryEntry,
)

# Opportunities
from app.schemas.opportunity import (
    Opportunity,
    OpportunityLifecycle,
    OpportunityParseRequest,
    OpportunityParseResponse,
    OpportunityType,
)

# Recommendations
from app.schemas.recommendation import (
    PathwayType,
    Recommendation,
    RecommendationRequest,
    RecommendationResponse,
    ScoreBreakdown,
)

# Roadmaps
from app.schemas.roadmap import (
    Roadmap,
    RoadmapRequest,
    RoadmapResponse,
    RoadmapStep,
    StepStatus,
    StepType,
)

# Market Demand
from app.schemas.market import (
    MarketDemandRequest,
    MarketDemandResponse,
    SectorDemand,
)

# Health & Speech
from app.schemas.health import HealthResponse
from app.schemas.speech import SpeechTranscribeRequest, SpeechTranscribeResponse

__all__ = [
    # Phase 3 — Ontology & Provenance
    "DataClassification",
    "OntologyRecord",
    "DataSourceRecord",
    "SourcePrecedence",
    # Phase 3 — Location
    "LocationRecord",
    # Phase 3 — Training Provider
    "AccreditationStatus",
    "ProviderType",
    "TrainingProvider",
    # Common
    "APIResponse",
    "EducationLevel",
    "EmploymentPreference",
    "ErrorDetail",
    "Gender",
    "GeographicLocation",
    "ProfileSource",
    "ServiceStatus",
    "SourceEvidence",
    "SourceType",
    "VerificationStatus",
    # Skills
    "GapStatus",
    "PriorityLevel",
    "RawSkill",
    "SkillNormalizationMethod",
    "SkillNormalizationResult",
    "SkillNormalizationStatus",
    "Skill",
    "SkillCategory",
    "SkillGap",
    "SkillProficiency",
    "SkillSource",
    # Occupations
    "EmploymentType",
    "Occupation",
    # Courses
    "NSQFCourse",
    # Eligibility
    "CriterionResult",
    "EligibilityResult",
    "EligibilityStatus",
    # Profiles
    "BeneficiaryProfile",
    "EducationEntry",
    "ProfileExtractRequest",
    "ProfileExtractResponse",
    "ProfileValidateRequest",
    "ProfileValidateResponse",
    "WorkHistoryEntry",
    # Opportunities
    "Opportunity",
    "OpportunityLifecycle",
    "OpportunityParseRequest",
    "OpportunityParseResponse",
    "OpportunityType",
    # Recommendations
    "PathwayType",
    "Recommendation",
    "RecommendationRequest",
    "RecommendationResponse",
    "ScoreBreakdown",
    # Roadmaps
    "Roadmap",
    "RoadmapRequest",
    "RoadmapResponse",
    "RoadmapStep",
    "StepStatus",
    "StepType",
    # Market
    "MarketDemandRequest",
    "MarketDemandResponse",
    "SectorDemand",
    # Health & Speech
    "HealthResponse",
    "SpeechTranscribeRequest",
    "SpeechTranscribeResponse",
]
