# ResumeMaker — AI-Powered Resume Optimization Platform

An AI-powered resume engineering platform that tailors your resume to any job description while preserving your template's layout and ensuring every claim is factually grounded.

## Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14 (App Router) + TypeScript + Tailwind CSS |
| Backend | Python 3.12 + FastAPI |
| Database | PostgreSQL 16 |
| AI | Google Gemini Flash (free tier default) |
| PDF | ReportLab |
| DOCX | python-docx |
| Auth | Custom JWT (Argon2id) |

## Quick Start

### Prerequisites
- Docker + Docker Compose
- Node.js 20+
- Python 3.12+

### 1. Clone and configure
```bash
cp .env.example .env
# Edit .env — set GEMINI_API_KEY at minimum
```

### 2. Start with Docker
```bash
docker-compose up --build
```

### 3. Run locally (without Docker)

**Backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn src.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### 4. Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
resumeMaker/
├── frontend/          # Next.js app
├── backend/           # FastAPI app
├── docs/              # Architecture and API docs
├── docker-compose.yml
└── .env.example
```

## Development Phases

- [x] Phase 0 — Requirements Analysis
- [x] Phase 1 — Architecture Design
- [ ] Phase 2 — Project Foundation (current)
- [ ] Phase 3 — Master Career Profile
- [ ] Phase 4 — Template Engine
- [ ] Phase 5 — JD Engine
- [ ] Phase 6 — Question Engine
- [ ] Phase 7 — Resume Optimizer
- [ ] Phase 8 — ATS Engine
- [ ] Phase 9 — Document Rendering
- [ ] Phase 10 — Visual Validation
- [ ] Phase 11 — Polish

## Key Principles

- **No hallucination**: Every resume claim traces to verified user data
- **Template fidelity**: Preserves layout, typography, and structure of uploaded templates
- **Transparent ATS scoring**: Deterministic rule-based scoring, not probabilistic AI guesses
- **Free-first**: Gemini Flash free tier by default; swap providers via environment variable
