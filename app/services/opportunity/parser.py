"""
Opportunity Parsing Service Interface and Placeholder.
Parses livelihood, job postings, and PM-AJAY project opportunities from raw announcements.
"""

from abc import ABC, abstractmethod
from app.core.exceptions import ServiceNotImplementedException
from app.schemas.opportunity import OpportunityParseRequest, OpportunityParseResponse


class BaseOpportunityParsingService(ABC):
    """Abstract base interface for opportunity parsing."""

    @abstractmethod
    async def parse_opportunities(self, request: OpportunityParseRequest) -> OpportunityParseResponse:
        """Parse raw announcement text into structured opportunity records."""
        pass


class OpportunityParsingService(BaseOpportunityParsingService):
    """Production service placeholder for opportunity parsing."""

    async def parse_opportunities(self, request: OpportunityParseRequest) -> OpportunityParseResponse:
        raise ServiceNotImplementedException(
            service_name="OpportunityParsingService.parse_opportunities",
            details={
                "content_length": len(request.raw_content),
                "scheme_context": request.scheme_context,
            },
        )
