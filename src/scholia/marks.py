"""Compute numeric marks from category assignments and a scheme."""

from __future__ import annotations

from scholia.exceptions import CategoryNotInSchemeError
from scholia.scheme import Scheme
from scholia.students import Student


def compute_question_marks(student: Student, scheme: Scheme) -> dict[str, int | None]:
    """Return each question's mark for a student.

    Returns ``None`` for any question with no category assigned yet.

    Raises:
        CategoryNotInSchemeError: if a non-empty category label recorded in
            ``students.csv`` does not exist in the corresponding question in
            ``scheme.yaml``.
    """
    result: dict[str, int | None] = {}
    for question_name in scheme.question_names():
        category_id = student.assignments.get(question_name, "")
        if not category_id:
            result[question_name] = None
            continue
        category = scheme.get_category(question_name, category_id)
        if category is None:
            question = scheme.questions.get(question_name)
            valid_categories = list(question.categories.keys()) if question else []
            raise CategoryNotInSchemeError(
                student_id=student.student_id,
                question_name=question_name,
                category_id=category_id,
                valid_categories=valid_categories,
            )
        result[question_name] = category.marks
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
