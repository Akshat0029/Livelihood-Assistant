"""
Speech Transcription Service Interface and Placeholder.
Converts beneficiary voice audio input into text transcript (e.g., via Bhashini or local ASR).
"""

from abc import ABC, abstractmethod
from app.core.exceptions import ServiceNotImplementedException
from app.schemas.speech import SpeechTranscribeRequest, SpeechTranscribeResponse


class BaseSpeechTranscriptionService(ABC):
    """Abstract base interface for speech transcription."""

    @abstractmethod
    async def transcribe(self, request: SpeechTranscribeRequest) -> SpeechTranscribeResponse:
        """Transcribe audio into text."""
        pass


class SpeechTranscriptionService(BaseSpeechTranscriptionService):
    """Production service placeholder for speech transcription."""

    async def transcribe(self, request: SpeechTranscribeRequest) -> SpeechTranscribeResponse:
        raise ServiceNotImplementedException(
            service_name="SpeechTranscriptionService.transcribe",
            details={
                "language_code": request.language_code,
                "audio_format": request.audio_format,
            },
        )
