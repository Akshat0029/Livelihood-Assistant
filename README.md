# Livelihood-Assistant

[![CI](https://github.com/Akshat0029/Livelihood-Assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/Akshat0029/Livelihood-Assistant/actions/workflows/ci.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg?logo=python)](https://python.org)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-e92063.svg?logo=pydantic)](https://docs.pydantic.dev)

**Smart India Hackathon 2026** | **Problem Statement 26097**  
*AI-Driven Voice Assistant for Livelihood Mapping and NSQF-Aligned Skilling Recommendations for SC Communities under PM-AJAY.*

---

## 📌 Project Overview
Livelihood-Assistant is a standalone AI backend service providing clean RESTful endpoints to empower beneficiaries from Scheduled Caste (SC) communities under the **Pradhan Mantri Anusuchit Jaati Abhyuday Yojana (PM-AJAY)**. The service extracts candidate profiles from natural voice conversations, validates eligibility against scheme criteria, maps competencies to **National Skills Qualifications Framework (NSQF)** standards, analyzes district-level labor market demand, and outputs personalized career progression roadmaps.

---

## 🏛 Canonical Domain Pipeline

The service models the complete livelihood journey through canonical, strongly-typed Pydantic v2 domain schemas:

```
BeneficiaryProfile
   ↓
Skills (RawSkill & Canonical Skill)
   ↓
Occupation (NCO/NOS Classifications)
   ↓
NSQF Course (Levels 1–10, Qualification Packs)
   ↓
Eligibility (Criteria matching with explicit UNKNOWN support)
   ↓
Opportunity (Wage & Self-Employment, Lifecycle: Reported → Active → Filled)
   ↓
Recommendation (Top pathways with multidimensional score breakdown)
   ↓
Skill Gap (Proficiency delta with priority levels)
   ↓
Roadmap (Ordered milestone steps, prerequisites & durations)
```

Every recommendation and factual assertion is traceable via a unified, timezone-aware `SourceEvidence` model.

### Phase 4: Skill normalization

`SkillNormalizationService` maps a `RawSkill` to the canonical `Skill` records loaded from `data/seed/skills.json`. It preserves the original input and returns the canonical ID/name, supporting name or alias, normalization method, and confidence. It applies exact matching, token-boundary phrase matching, and a conservative standard-library spelling fallback in that order. Existing aliases are the sole source for transliterated or multilingual variants; it does not invent translations or skills.

The normalizer is deterministic, rejects collisions, and returns `UNKNOWN` with no canonical fields for unresolved or below-threshold inputs. Configure `SKILL_NORMALIZATION_MIN_CONFIDENCE` (default `0.90`) and `SKILL_NORMALIZATION_PHRASE_CONFIDENCE` (default `0.95`) in the environment. The service has no LLM, ASR, embedding, database, or external-backend dependency; a future embedding matcher can be added as a separate fallback stage.

### Phase 5: Hybrid recommendation engine

`RecommendationService` joins canonical occupation, course, opportunity, and skill repositories into at most three deterministic pathways. It applies known education, employment-preference, explicit eligibility, and location/mobility constraints before scoring interest (25%), skills (20%), eligibility (20%), local opportunity (15%), labour demand (10%), and work preference (10%). Weights are environment-configurable and must total 1.0.

Only seed-backed evidence is used. Missing profile data produces `UNKNOWN` eligibility or a zero component score instead of an assumed pass/fail or demand signal; no market-demand data currently exists in the seed set. The component methods are isolated for a future semantic matcher, but Phase 5 uses no embeddings, LLMs, databases, or external services.

### Phase 6: LLM-assisted profile extraction

`POST /v1/profile/extract` uses the environment-only `GEMINI_API_KEY` with Gemini JSON mode solely to extract stated beneficiary facts from multilingual text. Provider output is an untrusted payload: it is strictly Pydantic-validated, rejected on malformed or invalid values, and its raw skill phrases are normalized through Phase 4 before a canonical `BeneficiaryProfile` is returned. The response preserves the original text, raw skills, confidence, and model metadata. Gemini never produces recommendations or canonical opportunities, courses, eligibility, schemes, salaries, or market data.

### Phase 7: Speech-to-text

`POST /v1/speech/transcribe` accepts base64 WAV, MP3, OGG, or WebM audio, validates the declared type, decoded bytes, and configured size limit, then delegates to a replaceable ASR provider. The included local multilingual Whisper adapter requires an explicitly provisioned `ASR_MODEL_PATH`; it does not download models or datasets. Its transcript, selected/detected language, optional confidence, and processing metadata can be passed directly as the Phase 6 `raw_text` input.

### Phase 8: Conversational livelihood interview

`POST /v1/interview/turn` is a state-light interview endpoint: callers send the prior `BeneficiaryProfile`, optional session ID, user turn, and explicitly unknown slots each time. It reuses Phase 6 extraction and Phase 4 normalization, merges only stated values, reports outstanding slots, and selects one deterministic, localized next question. It does not persist sessions, fabricate profile values, or generate recommendations.

### Phase 9: Skill gaps and career roadmap

`POST /v1/roadmap` accepts a canonical target occupation or selected Phase 5 recommendation. It compares canonical beneficiary skills to the target requirements, classifies acquired, missing, and unknown gaps, and creates ordered training or opportunity-application steps only where linked repository records support them. Missing course mappings, unavailable opportunities, and unknown skills are recorded as explicit limitations or blocked verification steps; no courses, certifications, vacancies, benefits, or eligibility claims are invented.

### Phase 10: Opportunity intelligence and local observations

`POST /v1/opportunities/parse` normalizes only a trusted structured opportunity record. It preserves raw occupation/skill values, source evidence, lifecycle, verification state, and synthetic markers; raw announcement text alone is retained but not inferred into a vacancy. `POST /v1/opportunities/match` filters active records against canonical profile skills, location/mobility, employment preference, and an optional occupation ID. `POST /v1/market/demand` reports location-scoped counts of active repository records as observation evidence—not a demand forecast, trend, salary estimate, or statistical claim. Synthetic/demo records are clearly identified in its scope limitations.

---

## 🏗 Repository Structure
- **`app/main.py`**: Application factory, middleware, CORS, and global exception handlers.
- **`app/core/`**: Configuration management (`BaseSettings`) and custom exception classes.
- **`app/routes/`**: FastAPI routers grouped under `/v1` prefix.
- **`app/schemas/`**: Canonical Pydantic v2 domain contracts:
  - `profile.py`: `BeneficiaryProfile`, `EducationEntry`, `WorkHistoryEntry`.
  - `skill.py`: `RawSkill`, `Skill`, `SkillGap`, categories and proficiencies.
  - `occupation.py`: `Occupation`, `EmploymentType`.
  - `course.py`: `NSQFCourse` with strict NSQF level (1–10) bounds.
  - `eligibility.py`: `EligibilityResult`, `CriterionResult`, `EligibilityStatus`.
  - `opportunity.py`: `Opportunity`, `OpportunityType`, `OpportunityLifecycle`.
  - `recommendation.py`: `Recommendation`, `PathwayType`, `ScoreBreakdown`.
  - `roadmap.py`: `Roadmap`, `RoadmapStep`, `StepType`, `StepStatus`.
  - `common.py`: `GeographicLocation`, `SourceEvidence`, core enums.
- **`app/services/`**: Abstract service interfaces (`ABC`) and placeholder implementations.
- **`app/rules/`**: Static NSQF level descriptors and PM-AJAY program criteria.
- **`app/data/`**: Ingestion loaders and repository interfaces without database coupling.
- **`tests/`**: Unit tests, schema validation, integration tests, and evaluation harnesses.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.11, 3.12, or 3.13
- Virtual environment (`venv` recommended)

### 2. Environment Setup
```bash
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create `.env` from template:
```bash
cp .env.example .env
```

### 3. Running Locally
Start the development server with auto-reload:
```bash
python scripts/run_dev.py
```
Or directly with Uvicorn:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Interactive API Documentation:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI JSON**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)
- **Health Check**: [http://127.0.0.1:8000/v1/health](http://127.0.0.1:8000/v1/health)

---

## 🧪 Running Tests

Execute the complete test suite:
```bash
pytest -v
```

---

## 📡 API Endpoints (Version 1)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/v1/health` | Service health status and subsystem registration |
| `POST` | `/v1/profile/extract` | Extract canonical `BeneficiaryProfile` and raw skills from text |
| `POST` | `/v1/profile/validate` | Evaluate candidate eligibility against PM-AJAY criteria |
| `POST` | `/v1/recommendations` | Generate canonical `Recommendation` records with score breakdowns |
| `POST` | `/v1/speech/transcribe` | Audio speech-to-text transcription interface |
| `POST` | `/v1/opportunities/parse` | Parse public circulars into canonical `Opportunity` records |
| `POST` | `/v1/market/demand` | Query district/regional market skill demand |
| `POST` | `/v1/roadmap` | Generate step-by-step career & skilling roadmaps |

---

## 📄 License
Licensed under the Apache-2.0 License.
