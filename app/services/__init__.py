"""Services module index aggregating all domain service implementations."""

from app.services.ai.extractor import ProfileExtractionService
from app.services.speech.transcriber import SpeechTranscriptionService
from app.services.matching.matcher import SkillMatchingService
from app.services.recommendation.recommender import RecommendationService
from app.services.market.demand import MarketDemandService
from app.services.roadmap.generator import RoadmapService
from app.services.normalization.skill_normalizer import SkillNormalizationService
from app.services.interview.service import LivelihoodInterviewService

__all__ = [
    "ProfileExtractionService",
    "SpeechTranscriptionService",
    "SkillMatchingService",
    "RecommendationService",
    "MarketDemandService",
    "RoadmapService",
    "SkillNormalizationService",
    "LivelihoodInterviewService",
]
