# DOGFOOD — Enterprise Hackathon Management Platform

[![CI/CD](https://github.com/DikshantDuggal/DOGFOOD/actions/workflows/ci.yml/badge.svg)](https://github.com/DikshantDuggal/DOGFOOD/actions)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg?logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL%20%7C%20Auth-3ECF8E.svg?logo=supabase&logoColor=white)](https://supabase.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**DOGFOOD** is an enterprise-grade, high-performance hackathon operating system and submission evaluation platform. Built with **FastAPI**, **Supabase (PostgreSQL & Auth)**, and **React + Vite**, DOGFOOD orchestrates end-to-end hackathon lifecycles: from team formation and multi-track project submissions to cryptographic judging, community voting, and automated leaderboard calculation.

---

## 🌟 Key Platform Features

### 1. 👥 Team Formation & Management
* **Dynamic Invite Codes:** Cryptographically unique join codes for team invitations.
* **Role-Based Membership:** Lead, contributor, and mentor role assignments.
* **Track Registration:** Multi-track hackathon allocation (e.g., AI/ML, Web3, FinTech, DevTools, Open Innovation).

### 2. 🚀 Project Submissions & Artifact Locking
* **Comprehensive Project Specs:** Titles, elevator summaries, markdown descriptions, GitHub repositories, video demo links, and tech stack tags.
* **Deadline Enforcement:** Automatic write-locking of submission records once judging commences.
* **Rich Project Showcase:** Public gallery with deterministic randomized shuffling to prevent presentation bias.

### 3. ⚖️ T2 Cryptographic Judging Engine
* **Multi-Criteria Scoring Rubrics:** Normalized multi-dimensional evaluations (Innovation, Technical Execution, Real-World Impact, UI/UX).
* **Ed25519 Scorecard Signing:** Cryptographic signature verification ensuring judge evaluations remain tamper-proof and auditable.
* **Normalized Aggregate Scoring:** Outlier dampening and automated ranking computation.

### 4. 🗳️ Sybil-Resistant Community Voting
* **Participant Voting:** Community voting portal with real-time tallying and anti-tamper constraints.
* **Audit Logging:** Administrative event stream tracking all scoring, voting, and status transitions.

### 5. 🚢 Production Infrastructure & Deployment
* **Docker & Docker Compose:** Orchestrated multi-container stack with health checks and volume persistence.
* **Cloud Ready on Render:** Complete `render.yaml` Blueprint definition with zero-downtime rolling deploys and automatic environment synchronization.

---

## 🏛️ System Architecture

```text
                           ┌────────────────────────────┐
                           │      React 18 + Vite       │
                           │   (Tailwind CSS Frontend)  │
                           └──────────────┬─────────────┘
                                          │
                                   REST / JSON (JWT)
                                          │
                                          ▼
                           ┌────────────────────────────┐
                           │      FastAPI Backend       │
                           │     (Python 3.11/3.12)     │
                           └──────┬──────────────┬──────┘
                                  │              │
                   SQLAlchemy ORM │              │ Ed25519
                                  ▼              ▼
                    ┌──────────────────┐   ┌──────────────────┐
                    │ Supabase Postgres│   │ Cryptographic    │
                    │   & Auth Engine  │   │ Score Verification│
                    └──────────────────┘   └──────────────────┘
```

---

## 📂 Repository Directory Layout

```text
DOGFOOD/
├── backend/
│   ├── app/
│   │   ├── api/             # API routes (events, teams, submissions, judges, votes, results)
│   │   │   └── dependencies.py # Supabase JWT validation & auth guards
│   │   ├── core/            # App configuration, database engine, security
│   │   ├── models/          # SQLAlchemy relational models
│   │   ├── schemas/         # Pydantic v2 validation schemas
│   │   ├── services/        # Judging engine, fixture loader, cryptographic verification
│   │   └── main.py          # FastAPI application entrypoint & middleware
│   ├── tests/               # Pytest suite & health validation probes
│   ├── Dockerfile           # Backend container image
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # UI components (cards, modals, inputs, layout)
│   │   ├── pages/           # Dashboard, Gallery, Judging, Voting, Submissions
│   │   ├── lib/             # API clients, Supabase SDK, runtime environment resolver
│   │   └── App.tsx          # React Router declarative routing
│   ├── Dockerfile           # Production Node build + Nginx static server
│   └── package.json         # Frontend dependencies
├── docker/
│   └── postgres/init.sql    # Local database initialization fallback
├── docs/
│   └── repo.md              # Repository architecture specification
├── docker-compose.yml       # Complete local microservices stack
├── render.yaml              # Render cloud infrastructure blueprint
└── repo.md                  # Comprehensive architectural map & team boundaries
```

---

## ⚡ Quickstart Guide

### 1. Environment Configuration

Clone the repository and copy the environment template:

```bash
git clone https://github.com/DikshantDuggal/DOGFOOD.git
cd DOGFOOD
cp .env.example .env
```

Configure your Supabase project credentials in `.env`:
```env
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_ANON_KEY="your-supabase-anon-key"
SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"
SUPABASE_JWT_SECRET="your-jwt-secret"
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/dogfood"
```

### 2. Running with Docker Compose (Recommended)

To start the full stack (FastAPI backend, React frontend, and local PostgreSQL database):

```bash
docker compose up --build
```

Access the running services:
* 🌐 **React Frontend Application:** [http://localhost:8080](http://localhost:8080) (or dev HMR on [http://localhost:5173](http://localhost:5173))
* ⚡ **FastAPI Backend API:** [http://localhost:8000](http://localhost:8000)
* 📖 **Interactive OpenAPI Documentation (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
* 🩺 **Backend Liveness Health Probe:** [http://localhost:8000/health](http://localhost:8000/health)
* 🗄️ **Database Readiness Health Probe:** [http://localhost:8000/health/db](http://localhost:8000/health/db)

### 3. Local Development (Without Docker)

#### Backend Setup:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup:
```bash
cd frontend
npm install
npm run dev
```

---

## 📡 Core API Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/health` | Liveness probe returning server health | ❌ |
| `GET` | `/health/db` | Database readiness check verifying active pool connection | ❌ |
| `GET` | `/api/events` | List active hackathon events and deadlines | ❌ |
| `POST` | `/api/events` | Create a new hackathon event (Admin only) | ✅ |
| `GET` | `/api/teams` | Retrieve user teams and membership status | ✅ |
| `POST` | `/api/teams/join`| Join a team using an invite code | ✅ |
| `GET` | `/api/submissions` | List all submitted projects (Randomized Gallery) | ❌ |
| `POST` | `/api/submissions` | Create or update a project submission | ✅ |
| `POST` | `/api/submissions/{id}/submit` | Lock and officially submit project for judging | ✅ |
| `GET` | `/api/judges/assignments` | List submissions assigned to the current judge | ✅ |
| `POST` | `/api/scores` | Submit signed rubric evaluation for a project | ✅ |
| `POST` | `/api/votes` | Cast a community vote for a project | ✅ |
| `GET` | `/api/results/{eventId}` | Retrieve finalized hackathon results and rankings | ❌ |

---

## ☁️ Deployment (Render Cloud Blueprint)

The project includes automated deployment definitions in `render.yaml`:

| Service | Type | Context | Live Target |
| :--- | :--- | :--- | :--- |
| **`dogfood-backend`** | Docker Web Service | Root (`.`) | FastAPI REST API Server |
| **`dogfood-frontend`** | Docker Web Service | `./frontend` | Nginx React SPA Client |

### Automatic Deploy:
1. Connect this repository to your **Render Dashboard**.
2. Create a **New Blueprint Instance** from `render.yaml`.
3. Set your Supabase environment secrets in the Render dashboard.
4. Render automatically triggers zero-downtime builds on every push to `main`.

---

## 🛡️ Team Architecture & Contributing

For full details on team branch workflows, domain ownership boundaries, and database schemas, please consult [repo.md](repo.md).
