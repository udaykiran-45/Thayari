from sqlalchemy import Column, Integer, String, Float, Text
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    college = Column(String(200), nullable=False)
    branch = Column(String(100), nullable=False)
    cgpa = Column(Float, nullable=False)
    graduation_year = Column(Integer, nullable=False)
    skills = Column(Text, nullable=False)   # stored as comma-separated
    about_me = Column(Text, nullable=True)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    company = Column(String(150), nullable=False)
    required_skills = Column(Text, nullable=False)  # comma-separated
    min_cgpa = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    graduation_year_min = Column(Integer, nullable=True)  # extra dimension