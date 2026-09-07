"""Candidate profile extraction and validation schemas for PM-AJAY beneficiaries."""

from typing import List, Optional
from pydantic import BaseModel, Field


class Demographics(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    community: Optional[str] = Field(default="SC", description="Target community group e.g., Scheduled Caste")
    state: Optional[str] = None
    district: Optional[str] = None
    pincode: Optional[str] = None
    household_income: Optional[float] = None


class EducationHistory(BaseModel):
    highest_qualification: Optional[str] = None
    field_of_study: Optional[str] = None
    year_completed: Optional[int] = None


class WorkExperience(BaseModel):
    title: Optional[str] = None
    industry_sector: Optional[str] = None
    years_experience: Optional[float] = 0.0
    skills_used: List[str] = Field(default_factory=list)


class CandidateProfile(BaseModel):
    candidate_id: Optional[str] = None
    demographics: Demographics = Field(default_factory=Demographics)
    education: EducationHistory = Field(default_factory=EducationHistory)
    work_experience: List[WorkExperience] = Field(default_factory=list)
    existing_skills: List[str] = Field(default_factory=list)
    aspirations: List[str] = Field(default_factory=list)
    preferred_language: str = "hi"


class ProfileExtractRequest(BaseModel):
    raw_text: str = Field(..., description="Unstructured voice transcript or text from candidate interview")
    language: str = Field(default="hi", description="ISO 639-1 language code (e.g., hi, en, ta, mr)")
    source: str = Field(default="voice_interview", description="Origin of the text")


class ProfileExtractResponse(BaseModel):
    extracted_profile: CandidateProfile
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    missing_critical_fields: List[str] = Field(default_factory=list)
    status: str = Field(default="pending_ai_implementation")


class ProfileValidateRequest(BaseModel):
    profile: CandidateProfile
    scheme: str = Field(default="PM-AJAY", description="Government scheme to validate against")


class EligibilityCheck(BaseModel):
    criterion: str
    is_eligible: bool
    reason: str


class ProfileValidateResponse(BaseModel):
    is_eligible: bool
    scheme: str
    checks: List[EligibilityCheck] = Field(default_factory=list)
    recommended_nsqf_levels: List[int] = Field(default_factory=list)
    validation_notes: List[str] = Field(default_factory=list)
