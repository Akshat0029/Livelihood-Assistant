"""Speech transcription routes."""

from fastapi import APIRouter, Depends, status
from app.schemas.speech import SpeechTranscribeRequest, SpeechTranscribeResponse
from app.services.speech.transcriber import (
    BaseSpeechTranscriptionService,
    SpeechTranscriptionService,
)

router = APIRouter(prefix="/speech", tags=["Speech & Voice"])


def get_speech_service() -> BaseSpeechTranscriptionService:
    return SpeechTranscriptionService()


@router.post(
    "/transcribe",
    response_model=SpeechTranscribeResponse,
    status_code=status.HTTP_200_OK,
    summary="Transcribe audio speech to text",
)
async def transcribe_speech(
    request: SpeechTranscribeRequest,
    service: BaseSpeechTranscriptionService = Depends(get_speech_service),
) -> SpeechTranscribeResponse:
    """Transcribe speech audio into text transcript."""
    return await service.transcribe(request)
