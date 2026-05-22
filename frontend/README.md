# Thaiyari — Mini Student Profile + Job Match Engine

A full-stack web app that lets students fill in their profile and instantly see job listings ranked by how well they match. Built for the Thaiyari take-home assignment.

---

## Quick Start (one command per terminal)

```bash
# Terminal 1 — backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 2 — frontend
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173.

> The SQLite database (`thaiyari.db`) is created automatically on first run. Job listings are seeded on startup if the table is empty.

---

## Project Structure

```
thaiyari-assignment/
├── backend/
│   ├── main.py              # FastAPI app, CORS, startup hook
│   ├── database.py          # SQLAlchemy engine + session
│   ├── seed.py              # Seeds 8 job listings on first run
│   ├── match_engine.py      # Scoring algorithm (pure functions, no DB)
│   ├── requirements.txt
│   ├── models/
│   │   └── __init__.py      # Student and Job SQLAlchemy models
│   ├── schemas/
│   │   └── __init__.py      # Pydantic request/response schemas
│   ├── routers/
│   │   ├── students.py      # POST /api/students, GET /api/students/:id
│   │   └── jobs.py          # GET /api/jobs, GET /api/match/:studentId
│   └── tests/
│       └── test_match_engine.py
│
└── frontend/
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── api/index.js        # Axios wrapper for all API calls
        ├── styles/global.css   # All styles in one file
        ├── components/
        │   ├── SkillTagInput.jsx  # Tag-style skill entry
        │   └── JobCard.jsx        # Job match card with skill gap info
        └── pages/
            ├── ProfileForm.jsx    # /
            └── Dashboard.jsx      # /dashboard/:studentId
```

---

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/api/students` | Create a new student profile |
| GET | `/api/students/:id` | Get a student by ID |
| GET | `/api/students` | List students (with `limit`, `offset`, `branch`, `skill` filters) |
| GET | `/api/jobs` | Get all job listings |
| GET | `/api/match/:studentId` | Get all jobs ranked by match score for a student |

All routes return proper HTTP status codes. Validation errors return 422, missing records return 404.

---

## Match Algorithm

The match score is a number from 0 to 100, made up of three components:

### 1. Skill Overlap — 50 pts max

```
skill_score = (matched_skills / required_skills) * 50
```

The most important factor. A student who has 4 of 5 required skills gets 40/50. This rewards depth of match rather than just having lots of skills.

### 2. CGPA Score — 30 pts max

If the student's CGPA is below the job's minimum: 0 pts (ineligible, but job is still shown with a warning).

If eligible:
- Base: 20 pts
- Bonus: up to 10 pts, scaled by how far above the minimum the student's CGPA is

The bonus means a 9.0 student applying to a 6.0-minimum job scores better than a 6.5 student. This mirrors how real recruiters think — exceeding the threshold is a positive signal.

### 3. Branch Relevance — 20 pts max

- 20 pts: exact or near-exact branch match (e.g. "Computer Science" matches "CS")
- 10 pts: partial match (e.g. student says "IT", job lists "Information Technology")
- 10 pts: if the job has no branch preference (neutral, not penalised)
- 0 pts: clear mismatch

Jobs without branch preferences (some product/analyst roles) give 10 pts to everyone, since those roles genuinely hire across backgrounds.

### Example

A CS student with CGPA 8.0, knowing Python + SQL + React, applying to a frontend role requiring React, JavaScript, HTML, CSS, REST APIs with min CGPA 6.5:
- Skill: 1/5 matched → 10 pts
- CGPA: eligible → 20 + ~5 bonus = ~25 pts  
- Branch: CS → full 20 pts
- **Total: ~55/100**

That's a fair reflection — they're a branch fit and CGPA qualifies, but they're missing most technical skills.

---

## Running Tests

```bash
cd backend
pytest tests/ -v
```

---

## How I Used AI

I used Claude to:
- Scaffold the initial FastAPI router structure and Pydantic schemas (saved ~30 min)
- Draft the initial CSS design system variables and typography choices
- Generate the seed job data (the 8 job listings with realistic descriptions)

**What I changed:**
- The scoring algorithm was AI-suggested as a simple weighted average. I restructured it into three separate, clearly-named functions (`compute_skill_score`, `compute_cgpa_score`, `compute_branch_score`) to make testing easier and the logic more auditable. The CGPA bonus tier (rewarding exceeding the minimum, not just meeting it) was my own addition — AI just had a binary eligible/ineligible.
- The CSS was heavily reworked. AI suggested a generic purple-gradient dark theme; I switched to a warm off-white (`#f5f2eb`) with an orange accent to give it a more editorial, less "SaaS template" feel.
- AI suggested Redux for state management. I skipped it entirely — React's `useState` is more than enough for this scope and keeps the code readable.

**One decision I overrode:**
AI suggested storing skills as a JSON array in SQLite. I used a comma-separated string instead. For this scale it's simpler, requires no JSON parsing at the DB layer, and is easier to filter on with `LIKE` queries. It's a tradeoff I'd revisit if this needed full-text search or complex skill intersection queries.
