'''from sqlalchemy import Column, Integer, String, Float, Text
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    college = Column(String(200), nullable=False)
    branch = Column(String(100), nullable=False)
    cgpa = Column(Float, nullable=False)
    graduation_year = Column(Integer, nullable=False)
    # store as comma-separated string, simple enough for this scope
    skills = Column(Text, nullable=False)
    about_me = Column(Text, nullable=False)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    company = Column(String(150), nullable=False)
    required_skills = Column(Text, nullable=False)  # comma-separated
    min_cgpa = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    # branch hints for relevance scoring, e.g. "CS,IT,ECE"
    relevant_branches = Column(Text, nullable=True)

'''














from pydantic import BaseModel, field_validator
from typing import Optional, List


class StudentCreate(BaseModel):
    name: str
    college: str
    branch: str
    cgpa: float
    graduation_year: int
    skills: List[str]
    about_me: Optional[str] = ""

    @field_validator("name", "college", "branch")
    @classmethod
    def not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be empty")
        if len(v) > 200:
            raise ValueError("Field too long (max 200 chars)")
        return v

    @field_validator("cgpa")
    @classmethod
    def valid_cgpa(cls, v: float) -> float:
        if not (0.0 <= v <= 10.0):
            raise ValueError("CGPA must be between 0 and 10")
        return v

    @field_validator("graduation_year")
    @classmethod
    def valid_year(cls, v: int) -> int:
        if not (2000 <= v <= 2035):
            raise ValueError("Graduation year seems invalid")
        return v

    @field_validator("skills")
    @classmethod
    def at_least_one_skill(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("At least one skill is required")
        return [s.strip().lower() for s in v if s.strip()]


class StudentResponse(BaseModel):
    id: int
    name: str
    college: str
    branch: str
    cgpa: float
    graduation_year: int
    skills: List[str]
    about_me: Optional[str]

    model_config = {"from_attributes": True}


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    required_skills: List[str]
    min_cgpa: float
    description: str
    graduation_year_min: Optional[int]

    model_config = {"from_attributes": True}


class MatchResult(BaseModel):
    job: JobResponse
    score: float
    matched_skills: List[str]
    missing_skills: List[str]
    why: str