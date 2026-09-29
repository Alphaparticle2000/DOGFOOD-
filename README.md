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

## Deployment (Render)

The stack is deployed as **two Docker web services** defined in `render.yaml`
(a Render Blueprint). Both build from this repository; the database remains the
existing Supabase Postgres instance.

| Service            | Dockerfile              | Build context | Live URL |
| ------------------ | ----------------------- | ------------- | --- |
| `dogfood-backend`  | `backend/Dockerfile`    | repo root     | `https://dogfood-backend-nksw.onrender.com` |
| `dogfood-frontend` | `frontend/Dockerfile`   | `./frontend`  | `https://dogfood-frontend-9sqy.onrender.com` |

### Current live deployment

The services above are **live**. They were created with `render_deploy.sh`
(Render API v1, `runtime: image`) pulling the public Docker Hub images
`supremesahil/dogfood-backend:latest` and `supremesahil/dogfood-frontend:latest`.
Render assigned **suffixed** subdomains (the base `dogfood-backend` /
`dogfood-frontend` names were already taken), so the URLs above are the real
ones — do not assume `…onrender.com` without the suffix.

> Secrets (`DATABASE_URL`, `SUPABASE_*`, `VITE_SUPABASE_*`) are injected as
> Render env vars per service, not baked into the images. The backend's
> `ALLOWED_ORIGINS` and the frontend's `VITE_API_URL` were set to the actual
> suffixed URLs so CORS resolves without hard-coded hosts.

### First-time deploy (Blueprint alternative)

1. Push `render.yaml` to `main`.
2. In Render: **Blueprints → New Blueprint Instance**, select this repo.
3. Render creates both services and builds them. Fill in the secrets that are
   marked `sync: false` (they are intentionally not stored in git):
   * backend — `SUPABASE_URL`, `SUPABASE_ANON_KEY`,
     `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_JWT_SECRET`, `DATABASE_URL`
   * frontend — `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`
4. `ALLOWED_ORIGINS` (backend) and `VITE_API_URL` (frontend) are wired
   automatically via `fromService`, so CORS resolves without hard-coded hosts.

Subsequent pushes to `main` trigger an automatic rebuild of both services.

### Frontend environment variables (important)

Vite inlines `import.meta.env` at **build** time, and Render does not pass plain
env vars into `docker build`. To work around this, the frontend container writes
a `/env.js` shim at startup containing every `VITE_*` variable present in the
container environment. Read config like this:

```ts
const apiUrl =
  import.meta.env.VITE_API_URL ||
  (window as any).__DOGFOOD_ENV__?.VITE_API_URL;
```

The React app is expected to append `/api` to `VITE_API_URL` itself, since
`RENDER_EXTERNAL_URL` cannot include a path prefix.

### Local production images

```bash
# Backend on :8000, frontend (nginx) on :8080
docker compose up --build

# Frontend with Vite HMR on :5173 instead
docker compose --profile dev up frontend-dev
```

---

## Team Ownership & Repository Rules

Please consult [repo.md](file:///c:/Projects/DOGFOOD-/repo.md) for detailed architectural boundaries, team ownership map, and Git branch workflows.
