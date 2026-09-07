"""Speech transcription and voice processing schemas."""

from typing import Optional
from pydantic import BaseModel, Field


class SpeechTranscribeRequest(BaseModel):
    audio_content_base64: Optional[str] = Field(
        default=None,
        description="Base64-encoded audio byte payload",
    )
    audio_url: Optional[str] = Field(
        default=None,
        description="Public/presigned URL to audio recording",
    )
    language_code: str = Field(
        default="hi",
        description="Source audio language (e.g. hi, ta, te, mr, bn, en)",
    )
    audio_format: str = Field(
        default="wav",
        description="Audio format encoding: wav, mp3, ogg, webm",
    )


class SpeechTranscribeResponse(BaseModel):
    transcript: str = ""
    detected_language: str = ""
    confidence: float = 0.0
    duration_seconds: Optional[float] = None
    status: str = Field(default="pending_ai_implementation")
