from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Student
from schemas import StudentCreate, StudentOut

router = APIRouter()


def skills_to_str(skills: List[str]) -> str:
    return ",".join(s.strip() for s in skills if s.strip())


def str_to_skills(skills_str: str) -> List[str]:
    return [s.strip() for s in skills_str.split(",") if s.strip()]


def student_to_out(student: Student) -> StudentOut:
    return StudentOut(
        id=student.id,
        name=student.name,
        college=student.college,
        branch=student.branch,
        cgpa=student.cgpa,
        graduation_year=student.graduation_year,
        skills=str_to_skills(student.skills),
        about_me=student.about_me,
    )


@router.post("/students", response_model=StudentOut, status_code=201)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    student = Student(
        name=payload.name,
        college=payload.college,
        branch=payload.branch,
        cgpa=payload.cgpa,
        graduation_year=payload.graduation_year,
        skills=skills_to_str(payload.skills),
        about_me=payload.about_me,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student_to_out(student)


@router.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_to_out(student)


# stretch goal: list with pagination + optional filters
@router.get("/students", response_model=List[StudentOut])
def list_students(
    limit: int = 10,
    offset: int = 0,
    branch: Optional[str] = None,
    skill: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Student)

    if branch:
        query = query.filter(Student.branch.ilike(f"%{branch}%"))

    if skill:
        query = query.filter(Student.skills.ilike(f"%{skill}%"))

    students = query.offset(offset).limit(limit).all()
    return [student_to_out(s) for s in students]
