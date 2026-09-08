"""Explicit capability registry for accepted text and voice languages.

An accepted identifier only means that the API can preserve and route text. It
does not imply translated interview content, LLM accuracy, ASR, or TTS support.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class LanguageCapabilityStatus(str, Enum):
    SUPPORTED = "supported"
    PARTIAL = "partial"
    FALLBACK = "fallback"
    UNSUPPORTED = "unsupported"
    NOT_RUNTIME_VERIFIED = "not_runtime_verified"


@dataclass(frozen=True)
class LanguageCapability:
    """Static, evidence-scoped capability statement for one language code."""

    internal_code: str
    display_name: str
    iso_639_3: Optional[str]
    native_name: Optional[str]
    language_family: Optional[str]
    text_input_supported: bool
    interview_supported: bool
    profile_extraction_supported: bool
    asr_supported: bool
    tts_supported: bool
    fallback_language: Optional[str]
    capability_status: LanguageCapabilityStatus
    notes: str
    asr_provider_code: Optional[str] = None


UNKNOWN_LANGUAGE = "unknown"
_LEGACY_TEXT_CODES = frozenset({
    "as", "bn", "brx", "doi", "gu", "kn", "kok", "ks", "mai", "ml", "mni",
    "mr", "ne", "or", "pa", "sa", "sd", "ta", "te", "ur",
})


_LANGUAGE_CAPABILITIES: dict[str, LanguageCapability] = {
    "en": LanguageCapability("en", "English", "eng", None, "Indo-European", True, True, True, True, False, None,
                              LanguageCapabilityStatus.SUPPORTED, "Existing English interview localization and Faster-Whisper language hint.", "en"),
    "hi": LanguageCapability("hi", "Hindi", "hin", None, "Indo-European", True, True, True, True, False, None,
                              LanguageCapabilityStatus.SUPPORTED, "Existing Hindi interview localization and Faster-Whisper language hint.", "hi"),
    # ISO 639-3 codes below are language identifiers, not Whisper hints. The
    # current Faster-Whisper adapter does not expose these as supported tokens.
    "sat": LanguageCapability("sat", "Santali", "sat", None, "Austroasiatic (Munda)", True, False, False, False, False, "hi",
                               LanguageCapabilityStatus.FALLBACK, "Text is preserved; Hindi interview fallback. Current Whisper adapter has no verified Santali hint."),
    "unr": LanguageCapability("unr", "Mundari", "unr", None, "Austroasiatic (Munda)", True, False, False, False, False, "hi",
                               LanguageCapabilityStatus.FALLBACK, "Text is preserved; Hindi interview fallback. Current Whisper adapter has no verified Mundari hint."),
    "kru": LanguageCapability("kru", "Kurukh / Oraon", "kru", None, "Dravidian", True, False, False, False, False, "hi",
                               LanguageCapabilityStatus.FALLBACK, "Text is preserved; Hindi interview fallback. Current Whisper adapter has no verified Kurukh hint."),
    "hoc": LanguageCapability("hoc", "Ho", "hoc", None, "Austroasiatic (Munda)", True, False, False, False, False, "hi",
                               LanguageCapabilityStatus.FALLBACK, "Text is preserved; Hindi interview fallback. Current Whisper adapter has no verified Ho hint."),
    "sck": LanguageCapability("sck", "Nagpuri / Nagpuria", "sck", None, "Indo-European", True, False, False, False, False, "hi",
                               LanguageCapabilityStatus.FALLBACK, "Uses the ISO 639-3 Sadri identifier used for Nagpuri/Sadri contexts; confirm speaker preference. Hindi interview fallback."),
    "kht": LanguageCapability("kht", "Khortha", "kht", None, "Indo-European", True, False, False, False, False, "hi",
                               LanguageCapabilityStatus.FALLBACK, "Text is preserved; Hindi interview fallback. Current Whisper adapter has no verified Khortha hint."),
}


def _legacy_capability(code: str) -> LanguageCapability:
    return LanguageCapability(
        code, code, None, None, None, True, False, False, False, False, "en",
        LanguageCapabilityStatus.PARTIAL,
        "Existing accepted text code; no verified localized interview or ASR capability is declared.",
    )


LANGUAGE_CAPABILITY_REGISTRY: dict[str, LanguageCapability] = {
    **{code: _legacy_capability(code) for code in _LEGACY_TEXT_CODES}, **_LANGUAGE_CAPABILITIES,
}
SUPPORTED_LANGUAGE_CODES = frozenset(LANGUAGE_CAPABILITY_REGISTRY)


def normalize_language_code(value: str, *, allow_unknown: bool = False) -> str:
    """Validate and normalize an accepted language identifier without translation."""
    if not isinstance(value, str):
        raise ValueError("language code must be a string")
    code = value.strip().casefold()
    if allow_unknown and code == UNKNOWN_LANGUAGE:
        return code
    if code not in LANGUAGE_CAPABILITY_REGISTRY:
        supported = ", ".join(sorted(SUPPORTED_LANGUAGE_CODES))
        raise ValueError(f"unsupported language code '{value}'; supported codes: {supported}")
    return code


def get_language_capability(value: str) -> LanguageCapability:
    """Return the registry declaration for a validated language code."""
    return LANGUAGE_CAPABILITY_REGISTRY[normalize_language_code(value)]


def normalize_detected_language(value: Optional[str]) -> str:
    """Map unusable provider detection metadata to explicit UNKNOWN."""
    if value is None:
        return UNKNOWN_LANGUAGE
    try:
        return normalize_language_code(value, allow_unknown=True)
    except ValueError:
        return UNKNOWN_LANGUAGE
