import csv

import pytest
import yaml


@pytest.fixture
def scheme_data() -> dict:
    return {
        "q1(a)": {
            "a": {"marks": 0, "feedback": "Did not attempt"},
            "b": {"marks": 8, "feedback": "Perfect solution"},
            "c": {"marks": 6, "feedback": "Omitted the derivative"},
        },
        "q1(b)": {
            "a": {"marks": 0, "feedback": "Did not attempt"},
            "b": {"marks": 10, "feedback": "Perfect solution"},
        },
    }


@pytest.fixture
def scheme_path(tmp_path, scheme_data):
    path = tmp_path / "scheme.yaml"
    with open(path, "w") as file_handle:
        yaml.dump(scheme_data, file_handle)
    return path


@pytest.fixture
def students_path(tmp_path):
    path = tmp_path / "students.csv"
    fieldnames = ["student_id", "q1(a)", "q1(b)"]
    rows = [
        {"student_id": "s001", "q1(a)": "b", "q1(b)": "b"},
        {"student_id": "s002", "q1(a)": "c", "q1(b)": "a"},
    ]
    with open(path, "w", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path

