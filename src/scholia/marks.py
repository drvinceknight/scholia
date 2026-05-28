"""Compute numeric marks from category assignments and a scheme."""

from __future__ import annotations

from scholia.exceptions import CategoryNotInSchemeError
from scholia.scheme import Scheme
from scholia.students import Student


def compute_criterion_marks(student: Student, scheme: Scheme) -> dict[str, int | None]:
    """Return each criterion's mark for a student.

    Returns ``None`` for any criterion with no category assigned yet.

    Raises:
        CategoryNotInSchemeError: if a non-empty category label recorded in
            ``students.csv`` does not exist in the corresponding criterion in
            ``scheme.yaml``.
    """
    result: dict[str, int | None] = {}
    for criterion_name in scheme.criterion_names():
        category_id = student.assignments.get(criterion_name, "")
        if not category_id:
            result[criterion_name] = None
            continue
        category = scheme.get_category(criterion_name, category_id)
        if category is None:
            criterion = scheme.criteria.get(criterion_name)
            valid_categories = list(criterion.categories.keys()) if criterion else []
            raise CategoryNotInSchemeError(
                student_id=student.student_id,
                criterion_name=criterion_name,
                category_id=category_id,
                valid_categories=valid_categories,
            )
        result[criterion_name] = category.marks
    return result


def compute_total_marks(student: Student, scheme: Scheme) -> int | None:
    """Return the sum of all criterion marks for a student.

    Returns ``None`` if any criterion is unassigned or the scheme is empty.
    """
    criterion_marks = compute_criterion_marks(student, scheme)
    values = list(criterion_marks.values())
    if not values or any(value is None for value in values):
        return None
    return sum(value for value in values if value is not None)
