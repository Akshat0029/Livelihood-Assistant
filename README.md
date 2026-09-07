# Livelihood-Assistant

[![CI](https://github.com/Akshat0029/Livelihood-Assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/Akshat0029/Livelihood-Assistant/actions/workflows/ci.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg?logo=python)](https://python.org)

**Smart India Hackathon 2026** | **Problem Statement 26097**  
*AI-Driven Voice Assistant for Livelihood Mapping and NSQF-Aligned Skilling Recommendations for SC Communities under PM-AJAY.*

---

## 📌 Project Overview
Livelihood-Assistant is a completely standalone AI backend service providing clean RESTful endpoints to empower beneficiaries from Scheduled Caste (SC) communities under the **Pradhan Mantri Anusuchit Jaati Abhyuday Yojana (PM-AJAY)**. The service extracts candidate profiles from natural voice conversations, validates eligibility against scheme criteria, maps competencies to **National Skills Qualifications Framework (NSQF)** standards, analyzes district-level labor market demand, and outputs personalized career progression roadmaps.

---

## 🏛 Architecture & Principles

### Standalone Design
This repository is completely independent:
- **No dependencies** on any other repository's codebase.
- **No direct database coupling** to external team databases (e.g., MongoDB).
- Exposes clean, standardized **REST APIs** over HTTP/JSON with OpenAPI specifications for integration with any web, mobile, or IVR interface.

### Layered Structure
- **`app/main.py`**: Application factory, middleware, CORS, and global exception handlers.
- **`app/core/`**: Configuration management (`BaseSettings`) and custom exception classes.
- **`app/routes/`**: FastAPI routers grouped under `/v1` prefix.
- **`app/schemas/`**: Pydantic v2 data contracts for strong typing and validation.
- **`app/services/`**: Abstract interfaces and modular service implementations (AI extraction, speech, matching, recommendations, market demand, roadmap).
- **`app/rules/`**: NSQF level descriptors and PM-AJAY program criteria.
- **`app/data/`**: Abstract data loaders and repositories for NSQF and local market records.
- **`tests/`**: Unit tests, API integration tests, and evaluation harnesses.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.11, 3.12, or 3.13
- Virtual environment (`venv` recommended)

### 2. Environment Setup
Clone the repository and set up a virtual environment:
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

Create `.env` from the template:
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

Once running, access:
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
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
| `POST` | `/v1/profile/extract` | Extract profile attributes from voice interview transcripts |
| `POST` | `/v1/profile/validate` | Check candidate eligibility against PM-AJAY scheme rules |
| `POST` | `/v1/recommendations` | Generate NSQF-aligned skilling & course recommendations |
| `POST` | `/v1/speech/transcribe` | Audio speech-to-text transcription interface |
| `POST` | `/v1/opportunities/parse` | Parse opportunities from notices and circulars |
| `POST` | `/v1/market/demand` | Query district/regional market skill demand |
| `POST` | `/v1/roadmap` | Generate step-by-step career & skilling roadmaps |

---

## 📄 License
Licensed under the Apache-2.0 License.
