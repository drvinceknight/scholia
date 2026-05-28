import pytest

from scholia.exceptions import CategoryNotInSchemeError
from scholia.marks import compute_criterion_marks, compute_total_marks
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


def test_compute_criterion_marks_complete(scheme, complete_student):
    marks = compute_criterion_marks(complete_student, scheme)
    assert marks["q1(a)"] == 8
    assert marks["q1(b)"] == 10


def test_compute_criterion_marks_incomplete(scheme, incomplete_student):
    marks = compute_criterion_marks(incomplete_student, scheme)
    assert marks["q1(a)"] == 6
    assert marks["q1(b)"] is None


def test_compute_criterion_marks_unknown_category(scheme, unknown_category_student):
    with pytest.raises(CategoryNotInSchemeError) as exc_info:
        compute_criterion_marks(unknown_category_student, scheme)
    error = exc_info.value
    assert error.student_id == "s003"
    assert error.criterion_name == "q1(a)"
    assert error.category_id == "z"
    assert sorted(error.valid_categories) == ["a", "b", "c"]


def test_compute_criterion_marks_unknown_category_message(
    scheme, unknown_category_student
):
    with pytest.raises(CategoryNotInSchemeError, match="'z'"):
        compute_criterion_marks(unknown_category_student, scheme)


def test_compute_criterion_marks_zero_marks(scheme):
    student = Student(
        student_id="s004",
        assignments={"q1(a)": "a", "q1(b)": "a"},
    )
    marks = compute_criterion_marks(student, scheme)
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
    with pytest.raises(CategoryNotInSchemeError):
        compute_total_marks(unknown_category_student, scheme)


def test_compute_total_marks_empty_scheme():
    empty_scheme = Scheme()
    student = Student(student_id="s001", assignments={})
    assert compute_total_marks(student, empty_scheme) is None
