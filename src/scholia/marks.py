"""Compute numeric marks from category assignments and a scheme."""

from __future__ import annotations

from scholia.scheme import Scheme
from scholia.students import Student


def compute_question_marks(
    student: Student, scheme: Scheme
) -> dict[str, int | None]:
    """Return each question's mark for a student.

    Returns ``None`` for any question with no valid category assigned.
    """
    result: dict[str, int | None] = {}
    for question_name in scheme.question_names():
        category_id = student.assignments.get(question_name, "")
        category = scheme.get_category(question_name, category_id)
        result[question_name] = category.marks if category is not None else None
    return result


def compute_total_marks(student: Student, scheme: Scheme) -> int | None:
    """Return the sum of all question marks for a student.

    Returns ``None`` if any question is unassigned or the scheme is empty.
    """
    question_marks = compute_question_marks(student, scheme)
    values = list(question_marks.values())
    if not values or any(value is None for value in values):
        return None
    return sum(value for value in values if value is not None)
