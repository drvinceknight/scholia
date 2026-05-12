import pytest

from scholia.marks import compute_question_marks, compute_total_marks
from scholia.scheme import Scheme
from scholia.students import Student


@pytest.fixture
def scheme(scheme_path):
    return Scheme.load(scheme_path)


@pytest.fixture
def complete_student():
    return Student(
        student_id="s001",
        assignments={"q1(a)": "b", "q1(b)": "b"},
    )


@pytest.fixture
def incomplete_student():
    return Student(
        student_id="s002",
        assignments={"q1(a)": "c"},
    )


@pytest.fixture
def unknown_category_student():
    return Student(
        student_id="s003",
        assignments={"q1(a)": "z", "q1(b)": "b"},
    )


def test_compute_question_marks_complete(scheme, complete_student):
    marks = compute_question_marks(complete_student, scheme)
    assert marks["q1(a)"] == 8
    assert marks["q1(b)"] == 10


def test_compute_question_marks_incomplete(scheme, incomplete_student):
    marks = compute_question_marks(incomplete_student, scheme)
    assert marks["q1(a)"] == 6
    assert marks["q1(b)"] is None


def test_compute_question_marks_unknown_category(scheme, unknown_category_student):
    marks = compute_question_marks(unknown_category_student, scheme)
    assert marks["q1(a)"] is None


def test_compute_question_marks_zero_marks(scheme):
    student = Student(
        student_id="s004",
        assignments={"q1(a)": "a", "q1(b)": "a"},
    )
    marks = compute_question_marks(student, scheme)
    assert marks["q1(a)"] == 0
    assert marks["q1(b)"] == 0


def test_compute_total_marks_complete(scheme, complete_student):
    total = compute_total_marks(complete_student, scheme)
    assert total == 18


def test_compute_total_marks_zero(scheme):
    student = Student(
        student_id="s004",
        assignments={"q1(a)": "a", "q1(b)": "a"},
    )
    assert compute_total_marks(student, scheme) == 0


def test_compute_total_marks_incomplete(scheme, incomplete_student):
    assert compute_total_marks(incomplete_student, scheme) is None


def test_compute_total_marks_unknown_category(scheme, unknown_category_student):
    assert compute_total_marks(unknown_category_student, scheme) is None


def test_compute_total_marks_empty_scheme():
    empty_scheme = Scheme()
    student = Student(student_id="s001", assignments={})
    assert compute_total_marks(student, empty_scheme) is None
