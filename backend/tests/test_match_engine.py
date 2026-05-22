import pytest
from match_engine import compute_match


def test_perfect_match():
    score, matched, missing, why = compute_match(
        student_skills=["python", "sql", "react"],
        student_cgpa=8.5,
        student_grad_year=2025,
        job_required_skills=["python", "sql", "react"],
        job_min_cgpa=7.0,
        job_grad_year_min=2025,
    )
    assert score == 100.0
    assert len(missing) == 0
    assert len(matched) == 3


def test_no_skill_match():
    score, matched, missing, why = compute_match(
        student_skills=["java"],
        student_cgpa=9.0,
        student_grad_year=2025,
        job_required_skills=["python", "sql"],
        job_min_cgpa=7.0,
        job_grad_year_min=2025,
    )
    assert score < 55  # only cgpa + grad year score
    assert len(matched) == 0
    assert len(missing) == 2


def test_cgpa_below_minimum_gives_partial():
    score, _, _, why = compute_match(
        student_skills=["python"],
        student_cgpa=6.0,
        student_grad_year=2025,
        job_required_skills=["python"],
        job_min_cgpa=8.0,
        job_grad_year_min=2025,
    )
    assert "below the minimum" in why
    assert score < 100


def test_wrong_grad_year_loses_points():
    score_new, _, _, _ = compute_match(
        student_skills=["python"],
        student_cgpa=8.0,
        student_grad_year=2026,
        job_required_skills=["python"],
        job_min_cgpa=7.0,
        job_grad_year_min=2025,
    )
    score_old, _, _, _ = compute_match(
        student_skills=["python"],
        student_cgpa=8.0,
        student_grad_year=2022,
        job_required_skills=["python"],
        job_min_cgpa=7.0,
        job_grad_year_min=2025,
    )
    assert score_new > score_old