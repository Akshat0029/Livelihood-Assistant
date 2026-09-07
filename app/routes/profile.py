"""Profile extraction and validation routes."""

from fastapi import APIRouter, Depends, status
from app.schemas.profile import (
    ProfileExtractRequest,
    ProfileExtractResponse,
    ProfileValidateRequest,
    ProfileValidateResponse,
)
from app.services.ai.extractor import BaseProfileExtractionService, ProfileExtractionService

router = APIRouter(prefix="/profile", tags=["Candidate Profile"])


def get_profile_service() -> BaseProfileExtractionService:
    return ProfileExtractionService()


@router.post(
    "/extract",
    response_model=ProfileExtractResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract candidate profile from unstructured voice transcript/text",
)
async def extract_candidate_profile(
    request: ProfileExtractRequest,
    service: BaseProfileExtractionService = Depends(get_profile_service),
) -> ProfileExtractResponse:
    """Extract candidate profile using extraction service."""
    return await service.extract_profile(request)


@router.post(
    "/validate",
    response_model=ProfileValidateResponse,
    status_code=status.HTTP_200_OK,
    summary="Validate candidate eligibility against PM-AJAY and NSQF guidelines",
)
async def validate_candidate_profile(
    request: ProfileValidateRequest,
    service: BaseProfileExtractionService = Depends(get_profile_service),
) -> ProfileValidateResponse:
    """Validate candidate profile using validation rules service."""
    return await service.validate_profile(request)
