import pytest

from scholia.students import STUDENTS_FILENAME, Student, Students


def test_load_students(students_path):
    students = Students.load(students_path)
    assert len(students.students) == 2
    assert students.students[0].student_id == "s001"
    assert students.students[0].assignments["q1(a)"] == "b"
    assert students.question_names == ["q1(a)", "q1(b)"]


def test_load_no_question_columns(tmp_path):
    path = tmp_path / "students.csv"
    path.write_text("student_id\ns001\n")
    students = Students.load(path)
    assert len(students.students) == 1
    assert students.question_names == []


def test_load_empty_roster(tmp_path):
    path = tmp_path / "students.csv"
    path.write_text("student_id\n")
    students = Students.load(path)
    assert students.students == []
    assert students.question_names == []


def test_save_roundtrip(tmp_path, students_path):
    students = Students.load(students_path)
    out_path = tmp_path / "out.csv"
    students.save(out_path)
    loaded = Students.load(out_path)
    assert len(loaded.students) == 2
    assert loaded.students[0].student_id == "s001"
    assert loaded.students[1].assignments["q1(b)"] == "a"


def test_save_fills_missing_assignments(tmp_path):
    path = tmp_path / "students.csv"
    path.write_text("student_id\ns001\n")
    students = Students.load(path)
    students.question_names = ["q1(a)"]
    out_path = tmp_path / "out.csv"
    students.save(out_path)
    loaded = Students.load(out_path)
    assert loaded.students[0].assignments["q1(a)"] == ""


def test_update_existing_question(students_path):
    students = Students.load(students_path)
    students.update("s001", "q1(a)", "a")
    assert students.students[0].assignments["q1(a)"] == "a"


def test_update_new_question(students_path):
    students = Students.load(students_path)
    students.update("s001", "q2(a)", "b")
    assert "q2(a)" in students.question_names
    assert students.students[0].assignments["q2(a)"] == "b"


def test_update_missing_student(students_path):
    students = Students.load(students_path)
    with pytest.raises(ValueError, match="'s999' not found"):
        students.update("s999", "q1(a)", "a")


def test_get_student_found(students_path):
    students = Students.load(students_path)
    student = students.get_student("s002")
    assert student is not None
    assert student.student_id == "s002"


def test_get_student_not_found(students_path):
    students = Students.load(students_path)
    assert students.get_student("s999") is None


def test_students_filename_constant():
    assert STUDENTS_FILENAME == "students.csv"


def test_student_dataclass():
    student = Student(student_id="s001")
    assert student.assignments == {}


def test_sync_headers_adds_new_question(tmp_path):
    path = tmp_path / "students.csv"
    path.write_text("student_id,q1(a)\ns001,b\n")
    students = Students.load(path)
    students.sync_headers(["q1(a)", "q1(b)"])
    assert students.question_names == ["q1(a)", "q1(b)"]
    assert students.students[0].assignments["q1(b)"] == ""
    assert students.students[0].assignments["q1(a)"] == "b"


def test_sync_headers_reorders(students_path):
    students = Students.load(students_path)
    students.sync_headers(["q1(b)", "q1(a)"])
    assert students.question_names == ["q1(b)", "q1(a)"]
    assert students.students[0].assignments["q1(a)"] == "b"


def test_sync_headers_appends_extra_columns(students_path):
    students = Students.load(students_path)
    students.sync_headers(["q1(a)"])
    assert students.question_names == ["q1(a)", "q1(b)"]


def test_sync_headers_no_students(scheme_path):
    from scholia.scheme import Scheme

    scheme = Scheme.load(scheme_path)
    students = Students(students=[], question_names=[])
    students.sync_headers(scheme.question_names())
    assert students.question_names == scheme.question_names()
