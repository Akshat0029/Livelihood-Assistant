"""
Profile Extraction Service Interface and Placeholder.
Extracts structured candidate profiles from unstructured conversational inputs.
"""

from abc import ABC, abstractmethod
from app.core.exceptions import ServiceNotImplementedException
from app.schemas.profile import (
    ProfileExtractRequest,
    ProfileExtractResponse,
    ProfileValidateRequest,
    ProfileValidateResponse,
)


class BaseProfileExtractionService(ABC):
    """Abstract base class defining profile extraction and validation interface."""

    @abstractmethod
    async def extract_profile(self, request: ProfileExtractRequest) -> ProfileExtractResponse:
        """Extract candidate demographics, education, skills, and aspirations from raw text."""
        pass

    @abstractmethod
    async def validate_profile(self, request: ProfileValidateRequest) -> ProfileValidateResponse:
        """Validate candidate profile eligibility against scheme rules."""
        pass


class ProfileExtractionService(BaseProfileExtractionService):
    """Production service placeholder for profile extraction."""

    async def extract_profile(self, request: ProfileExtractRequest) -> ProfileExtractResponse:
        raise ServiceNotImplementedException(
            service_name="ProfileExtractionService.extract_profile",
            details={"input_length": len(request.raw_text), "language": request.language},
        )

    async def validate_profile(self, request: ProfileValidateRequest) -> ProfileValidateResponse:
        raise ServiceNotImplementedException(
            service_name="ProfileExtractionService.validate_profile",
            details={"scheme": request.scheme},
        )
