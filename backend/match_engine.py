
from typing import List, Tuple


def compute_match(
    student_skills: List[str],
    student_cgpa: float,
    student_grad_year: int,
    job_required_skills: List[str],
    job_min_cgpa: float,
    job_grad_year_min: int,
) -> Tuple[float, List[str], List[str], str]:
#skills
    student_skill_set = set(s.lower() for s in student_skills)
    job_skill_set = set(s.lower() for s in job_required_skills)

    matched = list(student_skill_set & job_skill_set)
    missing = list(job_skill_set - student_skill_set)

    if job_skill_set:
        skill_score = (len(matched) / len(job_skill_set)) * 50
    else:
        skill_score = 50.0
#cgpa
    if job_min_cgpa > 0:
        cgpa_ratio = min(student_cgpa / job_min_cgpa, 1.0)
    else:
        cgpa_ratio = 1.0
    cgpa_score = cgpa_ratio * 30
#g_year
    grad_score = 20.0 if student_grad_year >= job_grad_year_min else 0.0

    total = round(skill_score + cgpa_score + grad_score, 1)

    why_parts = []
    why_parts.append(
        f"You match {len(matched)}/{len(job_skill_set)} required skills."
    )
    if student_cgpa >= job_min_cgpa:
        why_parts.append(f"Your CGPA of {student_cgpa} meets the minimum of {job_min_cgpa}.")
    else:
        why_parts.append(
            f"Your CGPA ({student_cgpa}) is below the minimum ({job_min_cgpa}) — partial credit applied."
        )
    if grad_score == 20.0:
        why_parts.append("Your graduation year fits this role's timeline.")
    else:
        why_parts.append("Your graduation year is earlier than preferred for this role.")

    why = " ".join(why_parts)
    return total, matched, missing, why