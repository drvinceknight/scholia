"""Full end-to-end integration tests.

Each test runs the complete workflow in a temporary directory that pytest
creates and tears down automatically.
"""

import csv

import yaml
from typer.testing import CliRunner

from scholia.cli import app

runner = CliRunner()

_SCHEME = {
    "q2": {
        "a": {"marks": 0, "feedback": "Did not attempt."},
        "b": {"marks": 5, "feedback": "Full marks."},
    },
    "q1": {
        "a": {"marks": 0, "feedback": "Did not attempt."},
        "b": {"marks": 10, "feedback": "Full marks."},
    },
}


def test_full_workflow_sorted_headers(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    assert runner.invoke(app, ["init"]).exit_code == 0
    assert (tmp_path / "scholia" / "scheme.yaml").exists()
    assert (tmp_path / "scholia" / "students.csv").exists()

    with open(tmp_path / "scholia" / "scheme.yaml", "w") as file_handle:
        yaml.dump(_SCHEME, file_handle, sort_keys=False)

    assert runner.invoke(app, ["update"]).exit_code == 0
    header = (tmp_path / "scholia" / "students.csv").read_text().splitlines()[0]
    assert header == "student_id,q1,q2,note"

    with open(tmp_path / "scholia" / "students.csv", "w", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=["student_id", "q1", "q2"])
        writer.writeheader()
        writer.writerow({"student_id": "s001", "q1": "b", "q2": "b"})
        writer.writerow({"student_id": "s002", "q1": "a", "q2": "b"})

    result = runner.invoke(app, ["mark"])
    assert result.exit_code == 0

    alice = (tmp_path / "scholia" / "feedback" / "s001.md").read_text()
    assert "# Feedback: s001" in alice
    assert "**Total marks:** 15" in alice  # q1=10 + q2=5

    bob = (tmp_path / "scholia" / "feedback" / "s002.md").read_text()
    assert "**Total marks:** 5" in bob  # q1=0 + q2=5

    summary = (tmp_path / "scholia" / "summary.md").read_text()
    assert "**Students marked:** 2" in summary
    assert "**Mean:** 10.00" in summary

    marks_csv = (tmp_path / "scholia" / "marks.csv").read_text()
    assert "s001,15" in marks_csv
    assert "s002,5" in marks_csv

    assert (tmp_path / "scholia" / "charts" / "distribution.png").exists()
    assert (tmp_path / "scholia" / "charts" / "cumulative.png").exists()
    assert (tmp_path / "scholia" / "charts" / "boxplot.png").exists()
    assert (tmp_path / "scholia" / "charts" / "correlation.png").exists()


def test_full_workflow_preserve_order(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner.invoke(app, ["init"])

    with open(tmp_path / "scholia" / "scheme.yaml", "w") as file_handle:
        yaml.dump(_SCHEME, file_handle, sort_keys=False)

    assert runner.invoke(app, ["update", "--preserve-order"]).exit_code == 0
    header = (tmp_path / "scholia" / "students.csv").read_text().splitlines()[0]
    assert header == "student_id,q2,q1,note"
