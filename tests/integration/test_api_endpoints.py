"""Integration tests for all initial API routes."""

from fastapi.testclient import TestClient


def test_profile_extract_endpoint(client: TestClient):
    """Verify POST /v1/profile/extract safely reports an unconfigured Gemini provider."""
    payload = {
        "raw_text": "Mera naam Rajesh hai, 10th pass hoon, solar work sikhna chahta hoon.",
        "language": "hi",
        "source": "voice_interview",
    }
    response = client.post("/v1/profile/extract", json=payload)
    assert response.status_code == 503
    data = response.json()
    assert data["success"] is False
    assert data["error"]["details"] == {"provider": "Gemini"}


def test_profile_extract_validation_error(client: TestClient):
    """Verify POST /v1/profile/extract returns 422 on invalid payload."""
    response = client.post("/v1/profile/extract", json={})
    assert response.status_code == 422


def test_profile_validate_endpoint(client: TestClient):
    """Verify POST /v1/profile/validate handles valid payload and returns 501 placeholder."""
    payload = {
        "profile": {
            "candidate_id": "cand_001",
            "demographics": {"name": "Aman", "community": "SC", "age": 21},
        },
        "scheme": "PM-AJAY",
    }
    response = client.post("/v1/profile/validate", json=payload)
    assert response.status_code == 501
    data = response.json()
    assert data["success"] is False
    assert "ProfileExtractionService.validate_profile" in data["error"]["message"]


def test_recommendations_endpoint(client: TestClient):
    """Verify POST /v1/recommendations returns deterministic Phase 5 results."""
    payload = {
        "profile": {
            "candidate_id": "cand_001",
            "existing_skills": ["welding"],
        },
        "target_sector": "Automotive",
        "max_recommendations": 3,
    }
    response = client.post("/v1/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["recommendations"] == []


def test_speech_transcribe_endpoint(client: TestClient):
    """Verify POST /v1/speech/transcribe handles valid payload and returns 501 placeholder."""
    payload = {
        "audio_content_base64": "UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=",
        "language_code": "hi",
        "audio_format": "wav",
    }
    response = client.post("/v1/speech/transcribe", json=payload)
    assert response.status_code == 501
    data = response.json()
    assert data["success"] is False
    assert "SpeechTranscriptionService.transcribe" in data["error"]["message"]


def test_opportunities_parse_endpoint(client: TestClient):
    """Verify POST /v1/opportunities/parse handles valid payload and returns 501 placeholder."""
    payload = {
        "raw_content": "PM-AJAY Special Drive: Free NSQF Level 4 training in Lucknow.",
        "scheme_context": "PM-AJAY",
    }
    response = client.post("/v1/opportunities/parse", json=payload)
    assert response.status_code == 501
    data = response.json()
    assert data["success"] is False
    assert "OpportunityParsingService.parse_opportunities" in data["error"]["message"]


def test_market_demand_endpoint(client: TestClient):
    """Verify POST /v1/market/demand handles valid payload and returns 501 placeholder."""
    payload = {
        "state": "Uttar Pradesh",
        "district": "Lucknow",
    }
    response = client.post("/v1/market/demand", json=payload)
    assert response.status_code == 501
    data = response.json()
    assert data["success"] is False
    assert "MarketDemandService.analyze_demand" in data["error"]["message"]


def test_roadmap_endpoint(client: TestClient):
    """Verify POST /v1/roadmap handles valid payload and returns 501 placeholder."""
    payload = {
        "profile": {
            "beneficiary_id": "cand_001",
            "traditional_skills": ["basic electrician"],
        },
        "target_occupation_id": "OCC-SOL-001",
        "timeframe_months": 6,
    }
    response = client.post("/v1/roadmap", json=payload)
    assert response.status_code == 501
    data = response.json()
    assert data["success"] is False
    assert "RoadmapService.generate_roadmap" in data["error"]["message"]


def test_profile_validate_validation_error(client: TestClient):
    """Verify POST /v1/profile/validate returns 422 on missing profile."""
    response = client.post("/v1/profile/validate", json={})
    assert response.status_code == 422


def test_recommendations_validation_error(client: TestClient):
    """Verify POST /v1/recommendations returns 422 on invalid max_recommendations or missing profile."""
    # Missing profile
    response = client.post("/v1/recommendations", json={"max_recommendations": 5})
    assert response.status_code == 422

    # Out of bounds max_recommendations
    response = client.post(
        "/v1/recommendations",
        json={"profile": {"candidate_id": "c1"}, "max_recommendations": 99},
    )
    assert response.status_code == 422


def test_speech_transcribe_validation_error(client: TestClient):
    """Verify POST /v1/speech/transcribe returns 422 on wrong types."""
    response = client.post(
        "/v1/speech/transcribe",
        json={"audio_content_base64": 12345},  # should be str
    )
    assert response.status_code == 422


def test_opportunities_parse_validation_error(client: TestClient):
    """Verify POST /v1/opportunities/parse returns 422 on missing raw_content."""
    response = client.post("/v1/opportunities/parse", json={})
    assert response.status_code == 422


def test_market_demand_validation_error(client: TestClient):
    """Verify POST /v1/market/demand returns 422 on missing state/district."""
    response = client.post("/v1/market/demand", json={"state": "Uttar Pradesh"})
    assert response.status_code == 422


def test_roadmap_validation_error(client: TestClient):
    """Verify POST /v1/roadmap returns 422 on missing target_role."""
    response = client.post(
        "/v1/roadmap",
        json={"profile": {"candidate_id": "c1"}},
    )
    assert response.status_code == 422
