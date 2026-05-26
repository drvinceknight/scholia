import pytest

from scholia.feedback import generate_all_feedback, generate_student_feedback
from scholia.scheme import Scheme
from scholia.students import Student, Students


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
def zero_marks_student():
    return Student(
        student_id="s003",
        assignments={"q1(a)": "a", "q1(b)": "a"},
    )


def test_feedback_complete_student(tmp_path, scheme, complete_student):
    generate_student_feedback(complete_student, scheme, tmp_path / "feedback")
    content = (tmp_path / "feedback" / "s001.md").read_text()
    assert "# Feedback: s001" in content
    assert "**Total marks:** 18" in content
    assert "**Marks:** 8" in content
    assert "Perfect solution" in content


def test_feedback_zero_marks(tmp_path, scheme, zero_marks_student):
    generate_student_feedback(zero_marks_student, scheme, tmp_path / "feedback")
    content = (tmp_path / "feedback" / "s003.md").read_text()
    assert "**Total marks:** 0" in content
    assert "**Marks:** 0" in content
    assert "Did not attempt" in content


def test_feedback_incomplete_student(tmp_path, scheme, incomplete_student):
    generate_student_feedback(incomplete_student, scheme, tmp_path / "feedback")
    content = (tmp_path / "feedback" / "s002.md").read_text()
    assert "**Total marks:** incomplete" in content
    assert "**Marks:** not yet marked" in content
    assert "**Marks:** 6" in content


def test_feedback_creates_directory(tmp_path, scheme, complete_student):
    feedback_dir = tmp_path / "nested" / "feedback"
    generate_student_feedback(complete_student, scheme, feedback_dir)
    assert (feedback_dir / "s001.md").exists()


def test_feedback_with_note(tmp_path, scheme, complete_student):
    complete_student.note = "Student requested an extension."
    generate_student_feedback(complete_student, scheme, tmp_path / "feedback")
    content = (tmp_path / "feedback" / "s001.md").read_text()
    assert "## Note" in content
    assert "Student requested an extension." in content


def test_feedback_without_note(tmp_path, scheme, complete_student):
    generate_student_feedback(complete_student, scheme, tmp_path / "feedback")
    content = (tmp_path / "feedback" / "s001.md").read_text()
    assert "## Note" not in content


def test_generate_all_feedback(tmp_path, scheme, students_path):
    students = Students.load(students_path)
    generate_all_feedback(students, scheme, tmp_path / "feedback")
    assert (tmp_path / "feedback" / "s001.md").exists()
    assert (tmp_path / "feedback" / "s002.md").exists()
