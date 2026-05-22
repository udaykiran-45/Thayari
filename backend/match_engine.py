
"""
Match scoring algorithm.

The score is out of 100, made up of three components:

1. Skill overlap (50 pts max)
   - (matched_skills / total_required_skills) * 50
   - Rewards students who cover more of what the job needs.

2. CGPA threshold (30 pts max)
   - If the student doesn't meet min CGPA → 0 points, job is still shown
     but marked ineligible (so the student knows).
   - If they meet it: base 20 pts, plus up to 10 bonus pts scaled by how
     much they exceed the minimum. Rationale: a 9.0 student applying to a
     6.0-minimum job is a stronger signal than a 6.1 student.

3. Branch relevance (20 pts max)
   - 20 pts if student's branch is in the job's relevant_branches list.
   - 10 pts if there's a partial match (e.g. "CS" in "Computer Science").
   - 0 if no relevance info is given (neutral, doesn't penalise).

This keeps things simple while rewarding well-rounded profiles.
"""
'''
from typing import List, Tuple


def normalise(text: str) -> str:
    return text.strip().lower()


def skill_overlap(student_skills: List[str], required_skills: List[str]) -> Tuple[List[str], List[str]]:
    student_set = {normalise(s) for s in student_skills}
    required_set = {normalise(r) for r in required_skills}

    matched = [r for r in required_skills if normalise(r) in student_set]
    missing = [r for r in required_skills if normalise(r) not in student_set]
    return matched, missing


def compute_skill_score(matched: List[str], required: List[str]) -> float:
    if not required:
        return 50.0  # no requirements → full marks
    return (len(matched) / len(required)) * 50


def compute_cgpa_score(student_cgpa: float, min_cgpa: float) -> Tuple[float, bool]:
    if student_cgpa < min_cgpa:
        return 0.0, False

    base = 20.0
    # bonus: how much above minimum, capped at 10 pts
    excess = student_cgpa - min_cgpa
    max_excess = 10.0 - min_cgpa if min_cgpa < 10.0 else 0.1
    bonus = min((excess / max(max_excess, 0.1)) * 10, 10.0)
    return base + bonus, True


def compute_branch_score(student_branch: str, relevant_branches: List[str]) -> float:
    if not relevant_branches:
        return 10.0  # neutral, give partial credit

    branch_lower = normalise(student_branch)
    for rb in relevant_branches:
        if normalise(rb) == branch_lower:
            return 20.0
        # partial match: "computer science" and "CS" type overlap
        if normalise(rb) in branch_lower or branch_lower in normalise(rb):
            return 10.0

    return 0.0


def build_explanation(matched: List[str], missing: List[str], cgpa_ok: bool,
                       student_cgpa: float, min_cgpa: float, branch_score: float) -> str:
    parts = []

    if matched:
        parts.append(f"You match {len(matched)}/{len(matched) + len(missing)} required skills.")
    else:
        parts.append("You don't match any required skills yet.")

    if cgpa_ok:
        parts.append(f"Your CGPA of {student_cgpa} meets the minimum of {min_cgpa}.")
    else:
        parts.append(f"Your CGPA ({student_cgpa}) is below the minimum ({min_cgpa}) — you can still apply but may be filtered.")

    if branch_score == 20.0:
        parts.append("Your branch is a strong fit for this role.")
    elif branch_score == 10.0:
        parts.append("Your branch is somewhat relevant to this role.")
    else:
        parts.append("Your branch isn't a direct match, but skills can compensate.")

    return " ".join(parts)


def score_match(student_skills: List[str], student_cgpa: float, student_branch: str,
                required_skills: List[str], min_cgpa: float, relevant_branches: List[str]):
    """
    Returns a dict with score (0-100), matched/missing skills, eligibility, explanation.
    """
    matched, missing = skill_overlap(student_skills, required_skills)

    skill_score = compute_skill_score(matched, required_skills)
    cgpa_score, cgpa_eligible = compute_cgpa_score(student_cgpa, min_cgpa)
    branch_score = compute_branch_score(student_branch, relevant_branches)

    total = round(skill_score + cgpa_score + branch_score, 1)
    # cap at 100 just in case
    total = min(total, 100.0)

    explanation = build_explanation(matched, missing, cgpa_eligible,
                                    student_cgpa, min_cgpa, branch_score)

    return {
        "score": total,
        "matched_skills": matched,
        "missing_skills": missing,
        "cgpa_eligible": cgpa_eligible,
        "why_this_match": explanation,
    }
'''
























"""
Match Algorithm
===============
Score is out of 100, composed of three dimensions:

1. Skill Overlap (50 pts)
   matched_skills / total_required_skills * 50
   Reason: Skills are the primary hiring filter.

2. CGPA Score (30 pts)
   - If student CGPA >= job min_cgpa: full 30 pts
   - If below: 0 pts (hard disqualifier partially softened)
   Actually we give partial credit: (student_cgpa / min_cgpa) * 30, capped at 30.
   Reason: Many jobs are flexible; a student at 6.9 for a 7.0 cutoff shouldn't be invisible.

3. Graduation Year Proximity (20 pts)
   Jobs prefer recent/upcoming graduates.
   If student grad year >= job graduation_year_min: full 20 pts, else 0.
   Reason: Freshness of talent matters for entry-level campus hiring.
"""

from typing import List, Tuple


def compute_match(
    student_skills: List[str],
    student_cgpa: float,
    student_grad_year: int,
    job_required_skills: List[str],
    job_min_cgpa: float,
    job_grad_year_min: int,
) -> Tuple[float, List[str], List[str], str]:

    student_skill_set = set(s.lower() for s in student_skills)
    job_skill_set = set(s.lower() for s in job_required_skills)

    matched = list(student_skill_set & job_skill_set)
    missing = list(job_skill_set - student_skill_set)

    # Dimension 1: Skill overlap
    if job_skill_set:
        skill_score = (len(matched) / len(job_skill_set)) * 50
    else:
        skill_score = 50.0

    # Dimension 2: CGPA
    if job_min_cgpa > 0:
        cgpa_ratio = min(student_cgpa / job_min_cgpa, 1.0)
    else:
        cgpa_ratio = 1.0
    cgpa_score = cgpa_ratio * 30

    # Dimension 3: Graduation year
    grad_score = 20.0 if student_grad_year >= job_grad_year_min else 0.0

    total = round(skill_score + cgpa_score + grad_score, 1)

    # Human-readable explanation
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