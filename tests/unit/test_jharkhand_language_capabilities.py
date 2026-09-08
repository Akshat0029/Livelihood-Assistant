"""Capability-bound Jharkhand local-language regression tests.

These tests deliberately validate routing/fallback metadata, not unverified
translations, ASR accuracy, or model capability.
"""

import asyncio
import base64
from pathlib import Path

import pytest

from app.core.exceptions import ValidationException
from app.data.loaders.domain_loaders import SkillLoader
from app.data.repositories.domain_repositories import SkillRepository
from app.schemas.interview import InterviewSlot
from app.schemas.language import (
    LANGUAGE_CAPABILITY_REGISTRY,
    LanguageCapabilityStatus,
    get_language_capability,
    normalize_language_code,
)
from app.schemas.profile import ProfileExtractRequest
from app.schemas.speech import SpeechTranscribeRequest
from app.services.ai.extractor import ProfileExtractionService
from app.services.ai.gemini import BaseStructuredExtractionProvider
from app.services.interview.service import LivelihoodInterviewService
from app.services.normalization.skill_normalizer import SkillNormalizationService
from app.services.speech.providers import ASRResult, BaseASRProvider
from app.services.speech.transcriber import SpeechTranscriptionService


JHARKHAND_CODES = {
    "Santali": "sat", "Mundari": "unr", "Kurukh / Oraon": "kru",
    "Ho": "hoc", "Nagpuri / Nagpuria": "sck", "Khortha": "kht",
}
WAV_BYTES = b"RIFF\x24\x00\x00\x00WAVEfmt " + b"\x00" * 32
WAV_BASE64 = base64.b64encode(WAV_BYTES).decode("ascii")


class FakeProvider(BaseStructuredExtractionProvider):
    provider_name = "fake-json"
    model_name = "fake"

    async def extract_json(self, prompt):
        return {"skills": [], "traditional_skills": [], "extraction_confidence": 0.0}


class FakeASR(BaseASRProvider):
    provider_name = "fake-asr"
    model_name = "fake"

    def __init__(self):
        self.calls = []

    async def transcribe(self, audio_bytes, audio_format, language_hint):
        self.calls.append((audio_bytes, audio_format, language_hint))
        return ASRResult(transcript="observed")


def extraction_service():
    repository = SkillRepository()
    for skill in SkillLoader(Path("data/seed/skills.json")).load().records:
        repository.add(skill)
    return ProfileExtractionService(FakeProvider(), SkillNormalizationService(repository))


def test_jharkhand_registry_uses_explicit_iso_639_3_identifiers_and_safe_capabilities():
    assert set(JHARKHAND_CODES.values()).issubset(LANGUAGE_CAPABILITY_REGISTRY)
    for display_name, code in JHARKHAND_CODES.items():
        capability = get_language_capability(code)
        assert capability.display_name == display_name
        assert capability.iso_639_3 == code
        assert capability.text_input_supported is True
        assert capability.interview_supported is False
        assert capability.profile_extraction_supported is False
        assert capability.asr_supported is False
        assert capability.tts_supported is False
        assert capability.fallback_language == "hi"
        assert capability.capability_status == LanguageCapabilityStatus.FALLBACK
        assert capability.native_name is None


@pytest.mark.parametrize("code", JHARKHAND_CODES.values())
def test_jharkhand_text_interview_uses_explicit_hindi_fallback_without_claiming_localization(code):
    question = LivelihoodInterviewService._question(InterviewSlot.SKILLS, code)
    assert question.language == "hi"
    assert question.requested_language == code
    assert question.fallback_language == "hi"
    assert question.used_fallback is True
    assert question.localization_status == "fallback"


@pytest.mark.parametrize("code", JHARKHAND_CODES.values())
def test_jharkhand_profile_extraction_preserves_input_and_capability_metadata(code):
    text = "[caller-supplied local-language text retained verbatim]"
    response = asyncio.run(extraction_service().extract_profile(ProfileExtractRequest(raw_text=text, language=code)))
    assert response.original_text == text
    assert response.extracted_profile.preferred_language == code
    assert response.extraction_metadata.input_language == code
    assert response.extraction_metadata.normalized_language == code
    assert response.extraction_metadata.language_capability_status == "fallback"
    assert response.extraction_metadata.fallback_language == "hi"


@pytest.mark.parametrize("code", JHARKHAND_CODES.values())
def test_jharkhand_asr_is_rejected_before_provider_and_never_sends_invalid_whisper_code(code):
    provider = FakeASR()
    request = SpeechTranscribeRequest(audio_content_base64=WAV_BASE64, audio_format="wav", language_code=code)
    with pytest.raises(ValidationException, match="ASR is not supported"):
        asyncio.run(SpeechTranscriptionService(provider).transcribe(request))
    assert provider.calls == []


def test_existing_hindi_and_english_capabilities_and_invalid_codes_remain_explicit():
    assert get_language_capability("hi").interview_supported is True
    assert get_language_capability("en").asr_provider_code == "en"
    assert normalize_language_code(" HI ") == "hi"
    with pytest.raises(ValueError, match="unsupported language"):
        normalize_language_code("fr")
