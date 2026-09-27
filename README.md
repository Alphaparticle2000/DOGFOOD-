# DOGFOOD — Hackathon Management Platform

A high-performance hackathon management platform built with **FastAPI**, **Supabase**, and **React + Vite**.

---

## Architecture Overview

* **Authentication & Identity:** Supabase Auth (JWT validation in FastAPI via `backend/app/api/dependencies.py`).
* **Database:** Supabase PostgreSQL with SQLAlchemy & connection pooling.
* **Storage:** Supabase Storage buckets for submission artifacts, pitch decks, and media.
* **Judging Engine:** Pure business logic judging engine in `backend/app/services/judging.py`.
* **DevOps & Infrastructure:** Docker, Docker Compose, automated health checks, and GitHub Actions CI.

---

## Quickstart Guide

### 1. Environment Setup

Copy the environment template and fill in your Supabase project credentials:

```bash
cp .env.example .env
```

Required Supabase credentials (from your Supabase Dashboard -> Project Settings -> API):
* `SUPABASE_URL`
* `SUPABASE_ANON_KEY`
* `SUPABASE_JWT_SECRET`
* `DATABASE_URL` (Direct port `5432` or Pooler port `6543`)

### 2. Running with Docker Compose (Recommended)

To start the entire stack (FastAPI backend and local fallback PostgreSQL):

```bash
docker compose up --build
```

The services will be available at:
* **FastAPI Backend:** [http://localhost:8000](http://localhost:8000)
* **Interactive API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Backend Health Check:** [http://localhost:8000/health](http://localhost:8000/health)
* **Database Readiness Probe:** [http://localhost:8000/health/db](http://localhost:8000/health/db)
* **Frontend:** [http://localhost:5173](http://localhost:5173)

### 3. Running Backend Locally (Without Docker)

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run FastAPI server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Running Tests

```bash
pytest -v
```

---

## Team Ownership & Repository Rules

Please consult [repo.md](file:///c:/Projects/DOGFOOD-/repo.md) for detailed architectural boundaries, team ownership map, and Git branch workflows.
