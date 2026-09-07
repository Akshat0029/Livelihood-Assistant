"""Unit tests for Pydantic schema validation."""

import pytest
from pydantic import ValidationError
from app.schemas.profile import CandidateProfile, Demographics, ProfileExtractRequest
from app.schemas.recommendation import QualificationPack, RecommendationRequest
from app.schemas.health import HealthResponse


def test_health_response_schema():
    """Verify HealthResponse schema validation."""
    response = HealthResponse(
        status="healthy",
        app_name="TestApp",
        version="1.0.0",
        environment="test",
        services={"api": "online"},
    )
    assert response.status == "healthy"
    assert response.services["api"] == "online"


def test_candidate_profile_defaults():
    """Verify CandidateProfile defaults and structure."""
    profile = CandidateProfile(
        candidate_id="cand_123",
        demographics=Demographics(name="Sunil Kumar", age=24, community="SC"),
        existing_skills=["carpentry"],
    )
    assert profile.candidate_id == "cand_123"
    assert profile.demographics.community == "SC"
    assert "carpentry" in profile.existing_skills


def test_profile_extract_request_validation():
    """Verify ProfileExtractRequest validation rules."""
    req = ProfileExtractRequest(raw_text="Namaste, main ITI electrician hoon.")
    assert req.raw_text == "Namaste, main ITI electrician hoon."
    assert req.language == "hi"

    # raw_text is required
    with pytest.raises(ValidationError):
        ProfileExtractRequest()


def test_recommendation_request_validation():
    """Verify RecommendationRequest schema bounds."""
    profile = CandidateProfile(candidate_id="c1")
    req = RecommendationRequest(profile=profile, max_recommendations=5)
    assert req.max_recommendations == 5

    # Out of bounds max_recommendations (> 20)
    with pytest.raises(ValidationError):
        RecommendationRequest(profile=profile, max_recommendations=50)


def test_qualification_pack_bounds():
    """Verify NSQF level boundary validation (1 to 10)."""
    qp = QualificationPack(
        qp_code="CON/Q0101",
        job_role="Mason General",
        nsqf_level=4,
        sector="Construction",
    )
    assert qp.nsqf_level == 4

    # Invalid NSQF level
    with pytest.raises(ValidationError):
        QualificationPack(
            qp_code="INVALID",
            job_role="Invalid Role",
            nsqf_level=12,
            sector="None",
        )
