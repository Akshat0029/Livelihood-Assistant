# API Specification (V1)

Base URL: `http://127.0.0.1:8000/v1`

---

### 1. Health Check
- **Endpoint**: `GET /v1/health`
- **Description**: Returns system operational status and registered subsystems.
- **Sample Response (200 OK)**:
```json
{
  "status": "healthy",
  "app_name": "Livelihood-Assistant-AI",
  "version": "0.1.0",
  "environment": "development",
  "services": {
    "api": "online",
    "ai_extractor": "registered",
    "speech_transcriber": "registered",
    "skill_matcher": "registered",
    "recommendation_engine": "registered",
    "market_demand": "registered",
    "roadmap_generator": "registered"
  }
}
```

---

### 2. Profile Extraction
- **Endpoint**: `POST /v1/profile/extract`
- **Description**: Extracts candidate profile information from raw conversational voice transcript.
- **Request Body**:
```json
{
  "raw_text": "Mera naam Rajesh hai, 10th pass hoon, electrician ka thoda kaam jaanta hoon.",
  "language": "hi",
  "source": "voice_interview"
}
```

---

### 3. Profile Validation
- **Endpoint**: `POST /v1/profile/validate`
- **Description**: Validates candidate demographic and educational eligibility against PM-AJAY and NSQF guidelines.
- **Request Body**:
```json
{
  "profile": {
    "demographics": { "community": "SC", "age": 22, "district": "Varanasi" },
    "existing_skills": ["electrician", "wiring"]
  },
  "scheme": "PM-AJAY"
}
```

---

### 4. Skilling & Livelihood Recommendations
- **Endpoint**: `POST /v1/recommendations`
- **Description**: Returns NSQF-aligned Qualification Packs matching the candidate's skills and aspirations.
- **Request Body**:
```json
{
  "profile": {
    "demographics": { "community": "SC" },
    "existing_skills": ["mobile repairing"]
  },
  "target_sector": "Electronics & Hardware",
  "max_recommendations": 5
}
```

---

### 5. Speech Transcription
- **Endpoint**: `POST /v1/speech/transcribe`
- **Description**: Accepts audio payloads (base64 or URL) and produces localized transcripts.
- **Request Body**:
```json
{
  "audio_content_base64": "<base64_encoded_audio>",
  "language_code": "hi",
  "audio_format": "wav"
}
```

---

### 6. Opportunity Parsing
- **Endpoint**: `POST /v1/opportunities/parse`
- **Description**: Parses unstructured public circulars, PM-AJAY notices, or job postings into structured opportunities.
- **Request Body**:
```json
{
  "raw_content": "Notice: Free NSQF Level 4 Solar Technician training under PM-AJAY for SC youth with stipend.",
  "scheme_context": "PM-AJAY"
}
```

---

### 7. Regional Market Demand
- **Endpoint**: `POST /v1/market/demand`
- **Description**: Queries regional and district skill market demand trends.
- **Request Body**:
```json
{
  "state": "Uttar Pradesh",
  "district": "Varanasi"
}
```

---

### 8. Career Roadmap Generation
- **Endpoint**: `POST /v1/roadmap`
- **Description**: Generates an actionable milestone progression roadmap for a target NSQF role.
- **Request Body**:
```json
{
  "profile": {
    "demographics": { "community": "SC" },
    "existing_skills": ["basic electrical wiring"]
  },
  "target_role": {
    "qp_code": "ELE/Q1401",
    "job_role": "Solar PV Installer",
    "nsqf_level": 4,
    "sector": "Electronics & Green Jobs"
  },
  "timeframe_months": 6
}
```
