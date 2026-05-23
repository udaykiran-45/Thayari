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

### 3. Graduation Year — 20 pts max

grad_score = 20 if student_grad_year >= job_grad_year_min else 0

If the student graduates on or after the job's minimum required year they get full 20 pts, otherwise 0. This ensures students are only matched to roles they can actually join in time.


### Example

A student with Python and SQL, CGPA 8.5, graduating 2025, applying to a job requiring Python, SQL, React with min CGPA 7.0 and min year 2025:

- Skill: 2/3 matched → 33 pts
- CGPA: 8.5/7.0 capped at 1.0 → 30 pts
- Grad year: 2025 >= 2025 → 20 pts
- Total: 83/100

---

## Running Tests

```bash
cd backend
pytest tests/ -v
```

---
## How I Used AI

I used Claude to:
- Scaffold the initial FastAPI router structure and Pydantic schemas
- Draft the initial CSS styling and design choices
- Generate the seed job data with realistic job descriptions

**What I changed:**
- The match algorithm structure was my own design. I wrote a single focused function called compute_match that handles skill overlap, CGPA ratio scoring, and graduation year check — each section clearly separated with comments.
- The CGPA scoring uses a ratio approach instead of a hard pass or fail. This was my own decision because partial credit keeps the score more meaningful and shows the student exactly how far they are from qualifying.
- AI suggested Redux for state management on the frontend. I skipped it entirely — useState is more than enough for this scope and keeps the code readable without unnecessary complexity.

**One decision I overrode:**
AI suggested storing skills as a JSON array in SQLite. I used a comma-separated string instead. It is simpler, has no parsing overhead, and is still filterable using LIKE queries. I would revisit this if the app needed complex skill intersection queries at scale.