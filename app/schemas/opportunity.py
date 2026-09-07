"""Opportunity parsing and structuring schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field


class ParsedOpportunity(BaseModel):
    title: str
    organization: Optional[str] = None
    opportunity_type: str = Field(..., description="e.g., job, apprenticeship, pm_ajay_grant, training")
    nsqf_level_required: Optional[int] = None
    eligible_communities: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    deadline: Optional[str] = None
    financial_assistance: Optional[str] = None


class OpportunityParseRequest(BaseModel):
    raw_content: str = Field(..., description="Unstructured announcement, circular, or scheme text")
    scheme_context: Optional[str] = Field(default="PM-AJAY", description="Specific scheme context")


class OpportunityParseResponse(BaseModel):
    opportunities: List[ParsedOpportunity] = Field(default_factory=list)
    total_parsed: int = 0
    status: str = Field(default="pending_ai_implementation")
