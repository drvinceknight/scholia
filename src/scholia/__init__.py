"""Scholia: a marking aid library."""

from scholia.exceptions import CategoryNotInSchemeError
from scholia.feedback import generate_all_feedback, generate_student_feedback
from scholia.marks import compute_question_marks, compute_total_marks
from scholia.scheme import Category, Question, Scheme
from scholia.stats import generate_marks_csv, generate_summary
from scholia.students import Student, Students

__all__ = [
    "Category",
    "CategoryNotInSchemeError",
    "Question",
    "Scheme",
    "Student",
    "Students",
    "compute_question_marks",
    "compute_total_marks",
    "generate_all_feedback",
    "generate_student_feedback",
    "generate_marks_csv",
    "generate_summary",
]
