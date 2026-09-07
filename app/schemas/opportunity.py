"""Canonical opportunity domain models supporting wage and self-employment."""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from app.schemas.common import GeographicLocation, SourceEvidence, VerificationStatus


class OpportunityType(str, Enum):
    WAGE_EMPLOYMENT = "wage_employment"
    SELF_EMPLOYMENT = "self_employment"
    APPRENTICESHIP = "apprenticeship"
    SCHEME_SUBSIDY = "scheme_subsidy"
    TRAINING_PROGRAM = "training_program"
    OTHER = "other"


class OpportunityLifecycle(str, Enum):
    REPORTED = "reported"
    VERIFIED = "verified"
    ACTIVE = "active"
    EXPIRED = "expired"
    FILLED = "filled"


class Opportunity(BaseModel):
    """Canonical opportunity record for wage jobs, apprenticeships, and PM-AJAY micro-enterprises."""

    opportunity_id: str = Field(..., description="Unique opportunity identifier")
    title: str = Field(..., description="Official title or description of role/grant")
    opportunity_type: OpportunityType = Field(
        ..., description="Wage employment vs. self-employment grant/pathway"
    )
    sector: str = Field(..., description="Industry domain or economic sector")
    description: Optional[str] = Field(
        default=None, description="Detailed job description or scheme terms"
    )
    required_skills: List[str] = Field(
        default_factory=list, description="Skills required for this opportunity"
    )
    location: GeographicLocation = Field(
        ..., description="Geographic location including district and optional coordinates"
    )
    employer_or_provider: Optional[str] = Field(
        default=None, description="Hiring organization, implementing agency, or DIC center"
    )
    source: Optional[SourceEvidence] = Field(
        default=None, description="Primary intake evidence reference"
    )
    collected_at: datetime = Field(
        ..., description="Timezone-aware intake/creation timestamp"
    )
    verification_status: VerificationStatus = Field(
        default=VerificationStatus.UNVERIFIED,
        description="Verification state of the opportunity posting",
    )
    last_verified_at: Optional[datetime] = Field(
        default=None, description="Timezone-aware timestamp of most recent verification check"
    )
    lifecycle_status: OpportunityLifecycle = Field(
        default=OpportunityLifecycle.REPORTED,
        description="Current lifecycle state (REPORTED -> VERIFIED -> ACTIVE -> EXPIRED/FILLED)",
    )
    financial_assistance: Optional[str] = Field(
        default=None, description="Salary, stipend, or PM-AJAY capital subsidy if applicable"
    )
    evidence: List[SourceEvidence] = Field(
        default_factory=list, description="Supporting documents, gazette notifications, or job ads"
    )

    @field_validator("collected_at", "last_verified_at")
    @classmethod
    def validate_tz(cls, dt: Optional[datetime]) -> Optional[datetime]:
        if dt is not None and (dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None):
            raise ValueError("Opportunity timestamps must be timezone-aware (e.g. UTC).")
        return dt


class OpportunityParseRequest(BaseModel):
    raw_content: str = Field(..., description="Unstructured announcement, circular, or scheme text")
    scheme_context: Optional[str] = Field(default="PM-AJAY", description="Specific scheme context")


class OpportunityParseResponse(BaseModel):
    parsed_opportunities: List[Opportunity] = Field(default_factory=list)
    total_parsed: int = 0
    status: str = Field(default="pending_ai_implementation")
