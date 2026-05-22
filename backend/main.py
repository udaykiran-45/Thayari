from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import engine, get_db
from match_engine import compute_match
from seed import seed

models.Base.metadata.create_all(bind=engine)
seed()

app = FastAPI(title="Thaiyari API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helpers ────────────────────────────────────────────────────────────────────

def skills_to_list(skills_str: str) -> List[str]:
    return [s.strip() for s in skills_str.split(",") if s.strip()]


def student_to_response(student: models.Student) -> schemas.StudentResponse:
    return schemas.StudentResponse(
        id=student.id,
        name=student.name,
        college=student.college,
        branch=student.branch,
        cgpa=student.cgpa,
        graduation_year=student.graduation_year,
        skills=skills_to_list(student.skills),
        about_me=student.about_me,
    )


def job_to_response(job: models.Job) -> schemas.JobResponse:
    return schemas.JobResponse(
        id=job.id,
        title=job.title,
        company=job.company,
        required_skills=skills_to_list(job.required_skills),
        min_cgpa=job.min_cgpa,
        description=job.description,
        graduation_year_min=job.graduation_year_min,
    )


# ── Student Endpoints ───────────────────────────────────────────────────────────

@app.post("/api/students", response_model=schemas.StudentResponse, status_code=201)
def create_student(payload: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = models.Student(
        name=payload.name,
        college=payload.college,
        branch=payload.branch,
        cgpa=payload.cgpa,
        graduation_year=payload.graduation_year,
        skills=",".join(payload.skills),
        about_me=payload.about_me or "",
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student_to_response(student)


@app.get("/api/students/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_to_response(student)


@app.get("/api/students", response_model=List[schemas.StudentResponse])
def list_students(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    branch: Optional[str] = Query(None),
    skill: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Student)
    if branch:
        query = query.filter(models.Student.branch.ilike(f"%{branch}%"))
    if skill:
        query = query.filter(models.Student.skills.ilike(f"%{skill.lower()}%"))
    students = query.offset(offset).limit(limit).all()
    return [student_to_response(s) for s in students]


# ── Job Endpoints ───────────────────────────────────────────────────────────────

@app.get("/api/jobs", response_model=List[schemas.JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    return [job_to_response(j) for j in jobs]


# ── Match Endpoint ──────────────────────────────────────────────────────────────

@app.get("/api/match/{student_id}", response_model=List[schemas.MatchResult])
def match_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    jobs = db.query(models.Job).all()
    results = []

    for job in jobs:
        score, matched, missing, why = compute_match(
            student_skills=skills_to_list(student.skills),
            student_cgpa=student.cgpa,
            student_grad_year=student.graduation_year,
            job_required_skills=skills_to_list(job.required_skills),
            job_min_cgpa=job.min_cgpa,
            job_grad_year_min=job.graduation_year_min or 2020,
        )
        results.append(
            schemas.MatchResult(
                job=job_to_response(job),
                score=score,
                matched_skills=matched,
                missing_skills=missing,
                why=why,
            )
        )

    results.sort(key=lambda r: r.score, reverse=True)
    return results