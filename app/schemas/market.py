"""Regional and district-level skill market demand schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field


class SectorDemand(BaseModel):
    sector_name: str
    demand_level: str = Field(..., description="High, Medium, Emerging")
    top_in_demand_roles: List[str] = Field(default_factory=list)
    average_monthly_wage: Optional[str] = None


class MarketDemandRequest(BaseModel):
    state: str = Field(..., description="State name (e.g., Uttar Pradesh, Bihar, Maharashtra)")
    district: str = Field(..., description="District name")
    sector_filter: Optional[str] = None


class MarketDemandResponse(BaseModel):
    state: str
    district: str
    top_sectors: List[SectorDemand] = Field(default_factory=list)
    growth_trends: List[str] = Field(default_factory=list)
    status: str = Field(default="pending_ai_implementation")
