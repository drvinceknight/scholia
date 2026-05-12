"""Generate per-student feedback markdown files."""

from __future__ import annotations

from pathlib import Path

from scholia.marks import compute_question_marks, compute_total_marks
from scholia.scheme import Scheme
from scholia.students import Student, Students


def generate_student_feedback(
    student: Student,
    scheme: Scheme,
    feedback_dir: Path,
) -> None:
    """Write a markdown feedback file to ``feedback_dir/<student_id>.md``."""
    feedback_dir.mkdir(parents=True, exist_ok=True)
    question_marks = compute_question_marks(student, scheme)
    total = compute_total_marks(student, scheme)

    lines: list[str] = [f"# Feedback: {student.student_id}", ""]

    if total is not None:
        lines += [f"**Total marks:** {total}", ""]
    else:
        lines += ["**Total marks:** incomplete", ""]

    lines += ["## Question breakdown", ""]

    for question_name, marks in question_marks.items():
        category_id = student.assignments.get(question_name, "")
        category = scheme.get_category(question_name, category_id)
        lines += [f"### {question_name}", ""]
        if marks is not None and category is not None:
            lines += [f"**Marks:** {marks}", "", category.feedback, ""]
        else:
            lines += ["**Marks:** not yet marked", ""]

    (feedback_dir / f"{student.student_id}.md").write_text("\n".join(lines))


def generate_all_feedback(
    students: Students,
    scheme: Scheme,
    feedback_dir: Path,
) -> None:
    """Write feedback files for all students in the roster."""
    for student in students.students:
        generate_student_feedback(student, scheme, feedback_dir)
