import csv

import pytest

from scholia.scheme import Scheme
from scholia.stats import (
    _generate_correlation_chart,
    generate_marks_csv,
    generate_summary,
)
from scholia.students import Students


@pytest.fixture
def scheme(scheme_path):
    return Scheme.load(scheme_path)


@pytest.fixture
def two_student_roster(students_path):
    # s001: q1(a)=b (8), q1(b)=b (10) => total 18
    # s002: q1(a)=c (6), q1(b)=a (0) => total 6
    return Students.load(students_path)


@pytest.fixture
def one_student_path(tmp_path):
    path = tmp_path / "one.csv"
    fieldnames = ["student_id", "q1(a)", "q1(b)"]
    with open(path, "w", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"student_id": "s001", "q1(a)": "b", "q1(b)": "b"})
    return path


@pytest.fixture
def empty_roster_path(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("student_id\n")
    return path


@pytest.fixture
def partial_roster_path(tmp_path):
    path = tmp_path / "partial.csv"
    fieldnames = ["student_id", "q1(a)", "q1(b)"]
    with open(path, "w", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"student_id": "s001", "q1(a)": "", "q1(b)": ""})
    return path


def test_summary_no_complete_students(tmp_path, scheme, empty_roster_path):
    students = Students.load(empty_roster_path)
    output = tmp_path / "summary.md"
    generate_summary(students, scheme, output)
    content = output.read_text()
    assert "No complete marks yet." in content
    assert "## Per-question breakdown" in content


def test_summary_two_students_no_charts(tmp_path, scheme, two_student_roster):
    output = tmp_path / "summary.md"
    generate_summary(two_student_roster, scheme, output)
    content = output.read_text()
    assert "**Students marked:** 2" in content
    assert "**Mean:** 12.00" in content
    assert "**Standard deviation:**" in content
    assert "charts" not in content


def test_summary_two_students_all_charts(tmp_path, scheme, two_student_roster):
    output = tmp_path / "summary.md"
    charts_dir = tmp_path / "charts"
    generate_summary(two_student_roster, scheme, output, charts_dir)
    content = output.read_text()
    assert "## Mark distribution" in content
    assert "## Cumulative mark distribution" in content
    assert "## Marks per criterion" in content
    assert "## Criterion mark correlations" in content
    assert (charts_dir / "distribution.png").exists()
    assert (charts_dir / "cumulative.png").exists()
    assert (charts_dir / "boxplot.png").exists()
    assert (charts_dir / "correlation.png").exists()


def test_summary_one_student_limited_charts(tmp_path, scheme, one_student_path):
    students = Students.load(one_student_path)
    output = tmp_path / "summary.md"
    charts_dir = tmp_path / "charts"
    generate_summary(students, scheme, output, charts_dir)
    assert (charts_dir / "distribution.png").exists()
    assert not (charts_dir / "cumulative.png").exists()
    assert not (charts_dir / "boxplot.png").exists()
    assert not (charts_dir / "correlation.png").exists()


def test_summary_single_question_no_correlation(tmp_path):
    import yaml

    scheme_path = tmp_path / "scheme.yaml"
    with open(scheme_path, "w") as file_handle:
        yaml.dump(
            {
                "q1": {
                    "a": {"marks": 0, "feedback": "x"},
                    "b": {"marks": 5, "feedback": "y"},
                }
            },
            file_handle,
        )
    students_path = tmp_path / "students.csv"
    with open(students_path, "w", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=["student_id", "q1"])
        writer.writeheader()
        writer.writerow({"student_id": "s001", "q1": "b"})
        writer.writerow({"student_id": "s002", "q1": "a"})
    scheme = Scheme.load(scheme_path)
    students = Students.load(students_path)
    output = tmp_path / "summary.md"
    charts_dir = tmp_path / "charts"
    generate_summary(students, scheme, output, charts_dir)
    assert (charts_dir / "distribution.png").exists()
    assert (charts_dir / "cumulative.png").exists()
    assert (charts_dir / "boxplot.png").exists()
    assert not (charts_dir / "correlation.png").exists()


def test_summary_one_student_stdev_zero(tmp_path, scheme, one_student_path):
    students = Students.load(one_student_path)
    output = tmp_path / "summary.md"
    generate_summary(students, scheme, output)
    content = output.read_text()
    assert "**Students marked:** 1" in content
    assert "**Standard deviation:** 0.00" in content


def test_summary_empty_category_assignment(tmp_path, scheme, partial_roster_path):
    students = Students.load(partial_roster_path)
    output = tmp_path / "summary.md"
    generate_summary(students, scheme, output)
    content = output.read_text()
    assert "No complete marks yet." in content


def test_summary_per_question_breakdown(tmp_path, scheme, two_student_roster):
    output = tmp_path / "summary.md"
    generate_summary(two_student_roster, scheme, output)
    content = output.read_text()
    assert "### q1(a)" in content
    assert "### q1(b)" in content
    assert "Perfect solution: 1 student(s) (8 marks)" in content
    assert "Omitted the derivative: 1 student(s) (6 marks)" in content


def test_summary_same_mark_different_feedback(tmp_path):
    import yaml

    # Two categories with identical marks but different feedback strings.
    scheme_path = tmp_path / "scheme.yaml"
    with open(scheme_path, "w") as file_handle:
        yaml.dump(
            {
                "q1": {
                    "b": {"marks": 8, "feedback": "Correct but concise"},
                    "c": {"marks": 8, "feedback": "Correct but verbose"},
                    "a": {"marks": 0, "feedback": "Did not attempt"},
                }
            },
            file_handle,
        )
    students_path = tmp_path / "students.csv"
    with open(students_path, "w", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=["student_id", "q1"])
        writer.writeheader()
        writer.writerow({"student_id": "s001", "q1": "b"})
        writer.writerow({"student_id": "s002", "q1": "c"})
    scheme = Scheme.load(scheme_path)
    students = Students.load(students_path)

    output = tmp_path / "summary.md"
    generate_summary(students, scheme, output)
    content = output.read_text()

    # Both students scored 8 but for distinct reasons: each appears separately.
    assert "Correct but concise: 1 student(s) (8 marks)" in content
    assert "Correct but verbose: 1 student(s) (8 marks)" in content
    # Total marks are still computed correctly.
    assert "**Students marked:** 2" in content
    assert "**Mean:** 8.00" in content


def test_generate_marks_csv_complete(tmp_path, scheme, two_student_roster):
    output = tmp_path / "marks.csv"
    generate_marks_csv(two_student_roster, scheme, output)
    rows = list(csv.DictReader(output.open()))
    assert rows[0] == {"student_id": "s001", "total_marks": "18"}
    assert rows[1] == {"student_id": "s002", "total_marks": "6"}


def test_generate_marks_csv_incomplete(tmp_path, scheme, partial_roster_path):
    students = Students.load(partial_roster_path)
    output = tmp_path / "marks.csv"
    generate_marks_csv(students, scheme, output)
    rows = list(csv.DictReader(output.open()))
    assert rows[0]["student_id"] == "s001"
    assert rows[0]["total_marks"] == ""


def test_correlation_chart_nan_handling(tmp_path):
    charts_dir = tmp_path / "charts"
    charts_dir.mkdir()
    # q1 identical for both students => zero variance => NaN correlation
    _generate_correlation_chart(
        ["q1", "q2"],
        [[5, 3], [5, 8]],
        charts_dir,
    )
    assert (charts_dir / "correlation.png").exists()
