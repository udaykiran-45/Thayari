from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Student, Job
from schemas import JobOut, MatchedJob
from match_engine import score_match

router = APIRouter()


def job_to_out(job: Job) -> JobOut:
    return JobOut(
        id=job.id,
        title=job.title,
        company=job.company,
        required_skills=[s.strip() for s in job.required_skills.split(",") if s.strip()],
        min_cgpa=job.min_cgpa,
        description=job.description,
        relevant_branches=[b.strip() for b in job.relevant_branches.split(",") if b.strip()] if job.relevant_branches else [],
    )


@router.get("/jobs", response_model=List[JobOut])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return [job_to_out(j) for j in jobs]


@router.get("/match/{student_id}", response_model=List[MatchedJob])
def match_jobs(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    jobs = db.query(Job).all()
    student_skills = [s.strip() for s in student.skills.split(",") if s.strip()]

    results = []
    for job in jobs:
        required_skills = [s.strip() for s in job.required_skills.split(",") if s.strip()]
        relevant_branches = (
            [b.strip() for b in job.relevant_branches.split(",") if b.strip()]
            if job.relevant_branches else []
        )

        match_data = score_match(
            student_skills=student_skills,
            student_cgpa=student.cgpa,
            student_branch=student.branch,
            required_skills=required_skills,
            min_cgpa=job.min_cgpa,
            relevant_branches=relevant_branches,
        )

        results.append(MatchedJob(
            job=job_to_out(job),
            score=match_data["score"],
            matched_skills=match_data["matched_skills"],
            missing_skills=match_data["missing_skills"],
            cgpa_eligible=match_data["cgpa_eligible"],
            why_this_match=match_data["why_this_match"],
        ))

    # sort by score descending
    results.sort(key=lambda x: x.score, reverse=True)
    return results
