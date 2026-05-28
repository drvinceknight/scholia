"""Custom exceptions raised by scholia."""

from __future__ import annotations


class CategoryNotInSchemeError(Exception):
    """Raised when a student's category assignment is not defined in the scheme.

    This means a non-empty category label appears in ``students.csv`` for a
    criterion, but that label has no matching entry in the corresponding
    criterion in ``scheme.yaml``.
    """

    def __init__(
        self,
        student_id: str,
        criterion_name: str,
        category_id: str,
        valid_categories: list[str],
    ) -> None:
        self.student_id = student_id
        self.criterion_name = criterion_name
        self.category_id = category_id
        self.valid_categories = valid_categories
        super().__init__(
            f"Student '{student_id}' has category '{category_id}' for criterion"
            f" '{criterion_name}', which is not defined in the scheme."
            f" Valid categories are: {valid_categories}."
        )
