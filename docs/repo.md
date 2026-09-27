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
│       └── ci.yml                                      [TO CREATE]
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── __init__.py                                 [TO CREATE]
│   │   │
│   │   ├── main.py                                     [TO CREATE]
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py                             [TO CREATE]
│   │   │   │
│   │   │   ├── dependencies.py                         [TO CREATE]
│   │   │   │
│   │   │   └── routes/
│   │   │       ├── __init__.py                          [TO CREATE]
│   │   │       ├── auth.py                              [TO CREATE]
│   │   │       ├── users.py                             [TO CREATE]
│   │   │       ├── events.py                            [TO CREATE]
│   │   │       ├── teams.py                             [TO CREATE]
│   │   │       ├── submissions.py                       [TO CREATE]
│   │   │       ├── judges.py                            [TO CREATE]
│   │   │       ├── rubrics.py                           [TO CREATE]
│   │   │       ├── scores.py                            [TO CREATE]
│   │   │       ├── votes.py                             [TO CREATE]
│   │   │       ├── comments.py                          [TO CREATE]
│   │   │       └── results.py                           [TO CREATE]
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py                              [TO CREATE]
│   │   │   ├── config.py                                [TO CREATE]
│   │   │   ├── database.py                              [TO CREATE]
│   │   │   └── security.py                              [TO CREATE]
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py                              [TO CREATE]
│   │   │   ├── user.py                                  [TO CREATE]
│   │   │   ├── event.py                                 [TO CREATE]
│   │   │   ├── team.py                                  [TO CREATE]
│   │   │   ├── submission.py                            [TO CREATE]
│   │   │   ├── judge.py                                 [TO CREATE]
│   │   │   ├── rubric.py                                [TO CREATE]
│   │   │   ├── score.py                                 [TO CREATE]
│   │   │   ├── vote.py                                  [TO CREATE]
│   │   │   ├── comment.py                               [TO CREATE]
│   │   │   └── audit_log.py                             [TO CREATE]
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py                              [TO CREATE]
│   │   │   ├── auth.py                                  [TO CREATE]
│   │   │   ├── user.py                                  [TO CREATE]
│   │   │   ├── event.py                                 [TO CREATE]
│   │   │   ├── team.py                                  [TO CREATE]
│   │   │   ├── submission.py                            [TO CREATE]
│   │   │   ├── judge.py                                 [TO CREATE]
│   │   │   ├── rubric.py                                [TO CREATE]
│   │   │   ├── score.py                                 [TO CREATE]
│   │   │   ├── vote.py                                  [TO CREATE]
│   │   │   └── comment.py                               [TO CREATE]
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
│   │   ├── __init__.py                                  [TO CREATE]
│   │   ├── test_auth.py                                  [TO CREATE]
│   │   ├── test_users.py                                 [TO CREATE]
│   │   ├── test_events.py                                [TO CREATE]
│   │   ├── test_teams.py                                 [TO CREATE]
│   │   ├── test_submissions.py                           [TO CREATE]
│   │   ├── test_judges.py                                [TO CREATE]
│   │   ├── test_scores.py                                [TO CREATE]
│   │   ├── test_votes.py                                 [TO CREATE]
│   │   └── test_results.py                               [TO CREATE]
│   │
│   ├── alembic/
│   │   ├── env.py                                       [TO CREATE]
│   │   ├── script.py.mako                               [TO CREATE]
│   │   └── versions/
│   │       └── ...                                      [TO CREATE]
│   │
│   ├── requirements.txt                                  [TO CREATE]
│   ├── Dockerfile                                        [TO CREATE]
│   └── pytest.ini                                        [TO CREATE]
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
│   │   │   └── api.ts                                   [TO CREATE]
│   │   │
│   │   ├── hooks/
│   │   │
│   │   ├── context/
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
├── docker-compose.yml                                    [TO CREATE]
│
├── docker/
│   └── postgres/
│       └── ...                                           [TO CREATE]
│
├── .env.example                                         [TO CREATE]
│
├── .gitignore                                             [EXISTING]
│
├── README.md                                              [EXISTING]
│
└── REPO_STRUCTURE.md                                      [THIS FILE]
```

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
├── models/
├── schemas/
├── core/
└── main.py
```

Responsibilities:

* FastAPI setup
* API routes
* Authentication
* Users
* Events
* Teams
* Submissions
* Judges
* Rubrics API
* Score API
* Votes
* Comments
* Results
* Database models
* Database relationships
* CRUD
* Migrations
* Backend API tests

Dikshant should call the existing judging engine rather than duplicate it.

Expected flow:

```text
API route
    ↓
Validation
    ↓
Judging service
    ↓
judging.py
    ↓
Result
```

---

# SAHIL — DEVOPS / INFRASTRUCTURE

Primary ownership:

```text
docker-compose.yml
Dockerfile
docker/
.github/workflows/
.env.example
```

Backend infrastructure:

```text
backend/app/core/
├── config.py
├── database.py
└── security.py
```

Potential security/dependency layer:

```text
backend/app/api/dependencies.py
```

Responsibilities:

* Docker
* Docker Compose
* PostgreSQL
* Container networking
* Environment configuration
* CI/CD
* Security configuration
* CORS
* Rate limiting
* RBAC infrastructure
* Health checks
* Backend/frontend integration
* Deployment readiness

Sahil should not rewrite Dikshant's application APIs.

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

Participant navbar:

```text
Dashboard
My Team
Submission
Gallery
Results
```

Judge/admin-specific:

```text
Judging
```

Responsibilities:

* UI
* Navigation
* Dashboard
* Login
* Team interface
* Submission interface
* Gallery
* Judging interface
* Results interface
* Responsive layout
* API integration

---

# SYSTEM FLOW

```text
                    ┌───────────────┐
                    │   FRONTEND    │
                    │   Himanshu    │
                    └───────┬───────┘
                            │
                         REST API
                            │
                            ▼
                    ┌───────────────┐
                    │    FASTAPI    │
                    │   Dikshant    │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
        Authentication   Judging       Database
              │          Engine
              │             │
              │          Mridul
              │
              └─────────────┼─────────────┘
                            │
                            ▼
                       PostgreSQL
```

Sahil provides the Docker, networking, security and CI/CD layer around the system.

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

# ARCHITECTURE RULE

Do not duplicate functionality between team members.

```text
FRONTEND
Himanshu
        │
        ▼
API
Dikshant
        │
        ▼
BUSINESS LOGIC
Mridul
        │
        ▼
DATABASE
Dikshant
        │
        ▼
INFRASTRUCTURE
Sahil
```

For judging:

```text
Himanshu
    │
    │ UI
    ▼
Dikshant
    │
    │ API
    ▼
Mridul
    │
    │ judging.py
    ▼
Database
```

---

# CURRENT IMPLEMENTATION STATUS

## Already implemented

```text
backend/app/services/__init__.py
backend/app/services/judging.py
backend/app/services/fixture_loader.py
backend/app/services/test_judging.py
backend/app/services/test_fixture_judging.py
fixtures.json
```

## Frontend currently being developed

```text
Login
Gallery
Dashboard
```

## Backend still to be implemented

```text
FastAPI application
Authentication
Users
Events
Teams
Submissions
Judges
Rubrics API
Score API integration
Votes
Comments
Results
Database
Migrations
```

## Infrastructure still to be implemented

```text
Docker
PostgreSQL
Docker Compose
CI/CD
Environment configuration
Security infrastructure
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
