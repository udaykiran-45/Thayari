"""Run once to seed job listings: python seed.py"""
from database import engine, SessionLocal
from models import Base, Job


JOBS = [
    {
        "title": "Software Development Engineer Intern",
        "company": "Amazon",
        "required_skills": "python,data structures,algorithms,sql,problem solving",
        "min_cgpa": 7.0,
        "description": "Work on large-scale distributed systems. Strong DSA fundamentals required.",
        "graduation_year_min": 2025,
    },
    {
        "title": "Frontend Developer",
        "company": "Razorpay",
        "required_skills": "react,javascript,html,css,rest api",
        "min_cgpa": 6.5,
        "description": "Build beautiful payment UIs used by millions of Indians.",
        "graduation_year_min": 2024,
    },
    {
        "title": "Data Analyst",
        "company": "Flipkart",
        "required_skills": "python,sql,excel,data visualization,statistics",
        "min_cgpa": 7.5,
        "description": "Analyze large datasets to drive business decisions.",
        "graduation_year_min": 2025,
    },
    {
        "title": "Backend Engineer",
        "company": "Zepto",
        "required_skills": "nodejs,sql,rest api,docker,problem solving",
        "min_cgpa": 6.0,
        "description": "Build high-throughput APIs for India's fastest grocery delivery.",
        "graduation_year_min": 2024,
    },
    {
        "title": "ML Engineer Trainee",
        "company": "CRED",
        "required_skills": "python,machine learning,numpy,pandas,statistics",
        "min_cgpa": 8.0,
        "description": "Work on recommendation and fraud detection models.",
        "graduation_year_min": 2025,
    },
    {
        "title": "Full Stack Developer",
        "company": "Postman",
        "required_skills": "react,nodejs,javascript,rest api,mongodb",
        "min_cgpa": 7.0,
        "description": "Shape the world's most popular API platform.",
        "graduation_year_min": 2024,
    },
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Job).count() == 0:
        for job_data in JOBS:
            db.add(Job(**job_data))
        db.commit()
        print(f"✅ Seeded {len(JOBS)} jobs.")
    else:
        print("Jobs already seeded.")
    db.close()


if __name__ == "__main__":
    seed()