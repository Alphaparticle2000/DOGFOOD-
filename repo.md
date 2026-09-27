# DOGFOOD — Full Repository Schema

> This is the repository architecture and ownership map for the DOGFOOD hackathon.
>
> Files marked `[EXISTING]` are already part of the project.
> Files marked `[TO CREATE]` are planned additions.
>
> Do not create planned files unless they are required by the implementation.

```text
DOGFOOD/
│
├── .git/
│
├── .github/
│   └── workflows/
│       └── ci.yml                                      [EXISTING — SAHIL]
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── __init__.py                                 [EXISTING — SAHIL]
│   │   │
│   │   ├── main.py                                     [EXISTING — SAHIL]
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py                             [EXISTING — SAHIL]
│   │   │   │
│   │   │   ├── dependencies.py                         [EXISTING — SAHIL]
│   │   │   │
│   │   │   └── routes/
│   │   │       ├── __init__.py                          [EXISTING — DIKSHANT]
│   │   │       ├── users.py                             [EXISTING — DIKSHANT]
│   │   │       ├── events.py                            [EXISTING — DIKSHANT]
│   │   │       ├── tracks.py                            [EXISTING — DIKSHANT]
│   │   │       ├── teams.py                             [EXISTING — DIKSHANT]
│   │   │       ├── submissions.py                       [TO CREATE — DIKSHANT]
│   │   │       ├── judges.py                            [TO CREATE — DIKSHANT]
│   │   │       ├── rubrics.py                           [TO CREATE — DIKSHANT]
│   │   │       ├── scores.py                            [TO CREATE — DIKSHANT]
│   │   │       ├── votes.py                             [TO CREATE — DIKSHANT]
│   │   │       ├── comments.py                          [TO CREATE — DIKSHANT]
│   │   │       └── results.py                           [TO CREATE — DIKSHANT]
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py                              [EXISTING — SAHIL]
│   │   │   ├── config.py                                [EXISTING — SAHIL]
│   │   │   ├── database.py                              [EXISTING — SAHIL]
│   │   │   └── security.py                              [EXISTING — SAHIL]
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py                              [EXISTING — DIKSHANT]
│   │   │   ├── user.py                                  [EXISTING — DIKSHANT]
│   │   │   ├── event.py                                 [EXISTING — DIKSHANT]
│   │   │   ├── track.py                                 [EXISTING — DIKSHANT]
│   │   │   ├── team.py                                  [EXISTING — DIKSHANT]
│   │   │   ├── team_member.py                           [EXISTING — DIKSHANT]
│   │   │   ├── submission.py                            [EXISTING — DIKSHANT]
│   │   │   ├── judge.py                                 [EXISTING — DIKSHANT]
│   │   │   ├── rubric.py                                [TO CREATE — DIKSHANT]
│   │   │   ├── score.py                                 [EXISTING — DIKSHANT]
│   │   │   ├── vote.py                                  [EXISTING — DIKSHANT]
│   │   │   ├── comment.py                               [EXISTING — DIKSHANT]
│   │   │   └── audit_log.py                             [EXISTING — DIKSHANT]
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py                              [EXISTING — DIKSHANT]
│   │   │   ├── user.py                                  [EXISTING — DIKSHANT]
│   │   │   ├── event.py                                 [EXISTING — DIKSHANT]
│   │   │   ├── track.py                                 [EXISTING — DIKSHANT]
│   │   │   ├── team.py                                  [EXISTING — DIKSHANT]
│   │   │   ├── judging.py                               [EXISTING — MRIDUL]
│   │   │   ├── submission.py                            [TO CREATE — DIKSHANT]
│   │   │   ├── judge.py                                 [TO CREATE — DIKSHANT]
│   │   │   ├── rubric.py                                [TO CREATE — DIKSHANT]
│   │   │   ├── score.py                                 [TO CREATE — DIKSHANT]
│   │   │   ├── vote.py                                  [TO CREATE — DIKSHANT]
│   │   │   └── comment.py                               [TO CREATE — DIKSHANT]
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py                              [EXISTING]
│   │   │   ├── judging.py                               [EXISTING — MRIDUL]
│   │   │   ├── fixture_loader.py                        [EXISTING — MRIDUL]
│   │   │   ├── test_judging.py                          [EXISTING — MRIDUL]
│   │   │   └── test_fixture_judging.py                  [EXISTING — MRIDUL]
│   │   │
│   │   └── utils/
│   │       ├── __init__.py                              [TO CREATE]
│   │       ├── validators.py                            [TO CREATE]
│   │       └── helpers.py                               [TO CREATE]
│   │
│   ├── tests/
│   │   ├── __init__.py                                  [EXISTING — SAHIL]
│   │   ├── test_health.py                               [EXISTING — SAHIL]
│   │   ├── test_users.py                                [EXISTING — DIKSHANT]
│   │   ├── test_events.py                               [EXISTING — DIKSHANT]
│   │   ├── test_teams.py                                [EXISTING — DIKSHANT]
│   │   ├── test_submissions.py                          [TO CREATE]
│   │   ├── test_judges.py                               [TO CREATE]
│   │   ├── test_scores.py                               [TO CREATE]
│   │   ├── test_votes.py                                [TO CREATE]
│   │   └── test_results.py                              [TO CREATE]
│   │
│   ├── alembic/
│   │   ├── env.py                                       [EXISTING — DIKSHANT]
│   │   ├── script.py.mako                               [EXISTING — DIKSHANT]
│   │   └── versions/
│   │       └── ...                                      [EXISTING — DIKSHANT]
│   │
│   ├── requirements.txt                                  [EXISTING — SAHIL]
│   ├── Dockerfile                                        [EXISTING — SAHIL]
│   └── pytest.ini                                        [EXISTING — SAHIL]
│
├── frontend/
│   │
│   ├── public/
│   │
│   ├── src/
│   │   │
│   │   ├── assets/
│   │   │
│   │   ├── components/
│   │   │   ├── Navbar/
│   │   │   ├── Sidebar/
│   │   │   ├── Card/
│   │   │   ├── Modal/
│   │   │   └── ...
│   │   │
│   │   ├── pages/
│   │   │   ├── Login/
│   │   │   ├── Dashboard/
│   │   │   ├── Team/
│   │   │   ├── Submission/
│   │   │   ├── Gallery/
│   │   │   ├── Judging/
│   │   │   └── Results/
│   │   │
│   │   ├── services/
│   │   │   ├── api.ts                                   [TO CREATE — HIMANSHU]
│   │   │   └── supabase.ts                              [TO CREATE — HIMANSHU]
│   │   │
│   │   ├── hooks/
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.tsx                          [TO CREATE — HIMANSHU]
│   │   │
│   │   ├── types/
│   │   │
│   │   ├── utils/
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── fixtures.json                                         [EXISTING]
│
├── docker-compose.yml                                    [EXISTING — SAHIL]
│
├── docker/
│   └── postgres/
│       └── init.sql                                      [EXISTING — SAHIL]
│
├── .env.example                                         [EXISTING — SAHIL]
│
├── .gitignore                                             [EXISTING]
│
├── README.md                                              [EXISTING]
│
└── repo.md                                                [THIS FILE]
```

---

# SUPABASE INTEGRATION ARCHITECTURE

The DOGFOOD platform integrates **Supabase** as the unified Identity, PostgreSQL Database, and Object Storage layer.

### 1. Authentication Flow (Supabase Auth)
* **Identity Provider:** Supabase Auth is the **sole source of truth** for user credentials, email confirmation, and OAuth (GitHub/Google).
* **Client Sign-In:** Himanshu's frontend uses `@supabase/supabase-js` to log in users directly.
* **Token Handshake:** Supabase returns an `access_token` (JWT). The frontend attaches this token as `Authorization: Bearer <token>` on all requests to Dikshant's FastAPI backend.
* **Backend Validation:** FastAPI uses `backend/app/core/security.py` (`verify_supabase_token`) and `backend/app/api/dependencies.py` (`get_current_user`, `require_role`) to verify the JWT using `SUPABASE_JWT_SECRET` (or dev debug bypass) and extract the user's role (`admin`, `judge`, `participant`).
* **NO Custom Password Auth in FastAPI:** Dikshant does **not** build custom password hashing, user registration with passwords, or JWT generation endpoints in FastAPI.

### 2. Database & Schema Conventions (Supabase PostgreSQL)
* **User Primary Key:** All database foreign keys referencing users (`user_id`) must use **UUID** (`UUID(as_uuid=True)` in SQLAlchemy) matching Supabase `auth.users(id)`. Never use integer IDs for users.
* **Public User Profile:** `models/user.py` maps to `public.users` storing application-specific profile data (display name, bio, avatar URL, team affiliations).
* **Alembic Schema Isolation:** Supabase manages internal schemas (`auth`, `storage`, `vault`, `extensions`). Dikshant's Alembic `env.py` **must restrict migrations strictly to the `public` schema** (`include_schemas=['public']`) to avoid dropping or altering Supabase system tables.
* **Connection Routing:**
  * **FastAPI Runtime:** Connects via `DATABASE_URL` (Supabase connection pooler or direct connection).
  * **Alembic Migrations:** Must run against direct connection (Port `5432` / Session mode), **not** the transaction pooler (Port `6543`), to support DDL locking.

### 3. File & Submission Storage (Supabase Storage)
* **Submissions Bucket:** Project demo media, screenshots, pitch decks, and code archives are stored in Supabase Storage buckets (e.g. `submissions`).
* **Upload Strategy:** Frontend uploads media directly to Supabase Storage using the user's authenticated Supabase session, storing the resulting public/signed URLs in Dikshant's `submissions` API.

---

# TEAM OWNERSHIP

## MRIDUL — JUDGING ENGINE

```text
backend/app/services/
├── __init__.py
├── judging.py
├── fixture_loader.py
├── test_judging.py
└── test_fixture_judging.py

fixtures.json
```

Responsibilities:

* Judging engine
* Rubric evaluation
* Criteria evaluation
* Score validation
* Judging rules
* Self-judging prevention
* Duplicate judging prevention
* Fixture-based judging
* Judging tests

### Important

There is currently **no `normalization.py`**.

Do not create a normalization service simply because it appears in an older architecture document.

If normalization is required later, add it only when the actual judging implementation needs it.

---

# DIKSHANT — APPLICATION BACKEND

Primary area:

```text
backend/app/
├── api/
│   └── routes/
│       ├── users.py
│       ├── events.py
│       ├── teams.py
│       ├── submissions.py
│       ├── judges.py
│       ├── rubrics.py
│       ├── scores.py
│       ├── votes.py
│       ├── comments.py
│       └── results.py
├── models/
├── schemas/
└── alembic/
```

Responsibilities:

* API routes (Users, Events, Teams, Submissions, Judges, Rubrics, Scores, Votes, Comments, Results)
* User profile endpoints (`/api/users/me` — tied to Supabase JWT `sub` claim)
* Database models & relationships (PostgreSQL via SQLAlchemy)
* **UUID user references:** All `user_id` columns typed as UUID to match Supabase Auth
* CRUD operations
* Alembic migrations (restricted to `public` schema)
* Integration with Mridul's judging engine (`judging.py`)
* Backend API tests

Dikshant should call the existing judging engine rather than duplicate it.

Expected flow:

```text
API route (authenticated via Supabase JWT)
    ↓
Role / Permission Validation (dependencies.py)
    ↓
Judging service
    ↓
judging.py
    ↓
Database commit
    ↓
Result
```

---

# SAHIL — DEVOPS / INFRASTRUCTURE

Primary ownership:

```text
docker-compose.yml
backend/Dockerfile
docker/
.github/workflows/
.env.example
```

Backend infrastructure & security layer:

```text
backend/app/
├── main.py
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
└── api/
    └── dependencies.py
```

Responsibilities:

* Docker & Docker Compose setup
* Supabase configuration & connection pooling integration
* Local fallback PostgreSQL container (with `uuid-ossp` and `pgcrypto` matching Supabase defaults)
* Container networking & health probes (`/health`, `/health/db`)
* Supabase JWT validation (`security.py`) & RBAC dependencies (`dependencies.py`)
* Environment configuration (`.env.example`, `config.py`)
* CI/CD GitHub Actions workflow (`ci.yml`)
* CORS middleware configuration for frontend Vite client
* Deployment readiness

Sahil should not rewrite Dikshant's application domain APIs.

---

# HIMANSHU — FRONTEND

Primary ownership:

```text
frontend/
```

Current UI work:

```text
Login
Gallery
Dashboard
```

Planned pages:

```text
Dashboard
My Team
Submission
Gallery
Judging
Results
```

Frontend Supabase integration:

```text
src/services/supabase.ts   (Supabase client initialization)
src/context/AuthContext.tsx (Supabase Auth session provider)
src/services/api.ts        (FastAPI Axios client with Supabase Bearer token)
```

Responsibilities:

* UI & UX components
* Supabase Client initialization & Auth (Login, Sign-Up, OAuth, Session state)
* Attaching Supabase Bearer JWT to backend API requests
* Direct submission asset uploads to Supabase Storage
* Dashboard, Team, Submission, Gallery, Judging, Results interfaces
* Responsive layout & cross-device compatibility

---

# SYSTEM FLOW

```text
                                 ┌─────────────────────────┐
                                 │   FRONTEND (Himanshu)   │
                                 │       React + Vite      │
                                 └───────────┬─────────────┘
                                             │
                       ┌─────────────────────┴─────────────────────┐
                       │                                           │
             1. Auth / Token Login                       2. REST API Calls
             & Direct File Uploads                       (Bearer Supabase JWT)
                       │                                           │
                       ▼                                           ▼
             ┌───────────────────┐                       ┌───────────────────┐
             │     SUPABASE      │                       │  FASTAPI BACKEND  │
             │   Auth & Storage  │                       │ (Dikshant/Sahil)  │
             └─────────┬─────────┘                       └─────────┬─────────┘
                       │                                           │
                       │                                   3. Validate JWT
                       │                                      & Check RBAC
                       │                                   (dependencies.py)
                       │                                           │
                       │                                   4. Call Judging
                       │                                       Logic (Mridul)
                       │                                           │
                       ▼                                           ▼
             ┌───────────────────────────────────────────────────────────────┐
             │                     SUPABASE POSTGRESQL                       │
             │                   (Managed Cloud Database)                    │
             │                                                               │
             │   - auth.users (Credentials & UUIDs managed by Supabase)      │
             │   - public.* (Teams, Events, Scores, Submissions by Dikshant) │
             └───────────────────────────────────────────────────────────────┘
```

Sahil provides the Docker, networking, security, Supabase configuration, and CI/CD layer around the entire stack.

---

# GIT BRANCHES

```text
main
│
├── mridul/backend-judging
├── himanshu/dashboard
├── dikshant/backend
└── sahil/devops
```

## Branch ownership

| Branch                   | Owner    | Purpose                   |
| ------------------------ | -------- | ------------------------- |
| `main`                   | Team     | Stable integrated version |
| `mridul/backend-judging` | Mridul   | Judging engine            |
| `himanshu/dashboard`     | Himanshu | Frontend/dashboard        |
| `dikshant/backend`       | Dikshant | FastAPI/backend           |
| `sahil/devops`           | Sahil    | Infrastructure/DevOps     |

---

# IMPORTANT GIT RULES

Never commit:

```text
.env
__pycache__/
*.pyc
node_modules/
secrets
API keys
passwords
tokens
```

Do not work directly on `main`.

Before starting:

```bash
git checkout main
git pull origin main
git checkout <your-branch>
```

After work:

```bash
git add .
git commit -m "Describe change"
git push
```

---

# ARCHITECTURE RULES

Do not duplicate functionality between team members.

```text
AUTHENTICATION & STORAGE
Supabase
        │
        ▼
FRONTEND
Himanshu
        │
        ▼
API ROUTING & MODELS
Dikshant
        │
        ▼
BUSINESS LOGIC
Mridul
        │
        ▼
DATABASE & SCHEMA
Dikshant (SQLAlchemy / Alembic public schema)
        │
        ▼
INFRASTRUCTURE & SECURITY
Sahil (Docker, JWT Auth, Database pooling, CI/CD)
```

For judging:

```text
Himanshu (Frontend)
    │
    │ UI (Score Submission Form)
    ▼
Dikshant (FastAPI)
    │
    │ API Route (/api/scores) + Bearer JWT Validation
    ▼
Mridul (Judging Engine)
    │
    │ judging.py (Validation, criteria checks, self-judging prevention)
    ▼
Database (Supabase PostgreSQL)
```

---

# CURRENT IMPLEMENTATION STATUS

## Implemented (Mridul — Judging)

```text
backend/app/services/__init__.py
backend/app/services/judging.py
backend/app/services/fixture_loader.py
backend/app/services/test_judging.py
backend/app/services/test_fixture_judging.py
fixtures.json
```

## Implemented (Sahil — DevOps & Core Infrastructure)

```text
backend/app/__init__.py
backend/app/main.py
backend/app/api/__init__.py
backend/app/api/dependencies.py
backend/app/core/__init__.py
backend/app/core/config.py
backend/app/core/database.py
backend/app/core/security.py
backend/requirements.txt
backend/Dockerfile
docker-compose.yml
docker/postgres/init.sql
.env.example
.github/workflows/ci.yml
```

## Frontend currently being developed (Himanshu)

```text
Login
Gallery
Dashboard
Supabase client integration
```

## Implemented (Dikshant — Backend Application Core)

```text
backend/app/models/user.py (UUID primary key matching Supabase auth.users)
backend/app/models/event.py
backend/app/models/track.py
backend/app/models/team.py
backend/app/models/team_member.py
backend/app/models/judge.py
backend/app/models/submission.py
backend/app/models/score.py
backend/app/models/vote.py
backend/app/models/comment.py
backend/app/models/audit.py
backend/app/schemas/user.py
backend/app/schemas/event.py
backend/app/schemas/track.py
backend/app/schemas/team.py
backend/app/api/routes/users.py (/api/users/me profile sync)
backend/app/api/routes/events.py (Events & Tracks CRUD + RBAC)
backend/app/api/routes/tracks.py (Tracks CRUD + RBAC)
backend/app/api/routes/teams.py (Teams & Team Members CRUD + Lead RBAC)
backend/alembic/env.py (configured for public schema isolation)
backend/alembic/versions/0ec25862acc1_initial_schema.py
backend/tests/test_users.py
backend/tests/test_events.py
backend/tests/test_teams.py
```

## Backend still to be implemented (Dikshant)

```text
API routes (submissions, judges, rubrics, scores, votes, comments, results)
Integration with judging.py
```

---

# DO NOT INVENT FILES

This document intentionally separates the actual implementation from the final architecture.

If a file does not exist, do not assume it exists just because it appears in the planned tree.

When a new file is actually created:

1. Add it to the repository.
2. Assign an owner.
3. Update this document.
4. Commit the documentation change.

The repository itself remains the source of truth.
