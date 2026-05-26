import csv

import pytest
import yaml
from typer.testing import CliRunner

from scholia.cli import app

runner = CliRunner()


@pytest.fixture
def chdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _write_scheme(path, scheme_data):
    with open(path, "w") as file_handle:
        yaml.dump(scheme_data, file_handle)


def _write_scheme_unordered(path):
    with open(path, "w") as file_handle:
        yaml.dump(
            {
                "q2": {"a": {"marks": 0, "feedback": "x"}},
                "q1": {"a": {"marks": 5, "feedback": "y"}},
            },
            file_handle,
            sort_keys=False,
        )


def _write_students(path, rows):
    if not rows:
        path.write_text("student_id\n")
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_init_creates_files(chdir):
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert (chdir / "scholia" / "scheme.yaml").exists()
    assert (chdir / "scholia" / "students.csv").exists()
    assert "Created scholia/scheme.yaml" in result.output
    assert "Created scholia/students.csv" in result.output


def test_init_skips_existing_files(chdir):
    runner.invoke(app, ["init"])
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "already exists" in result.output


def test_update_syncs_headers_sorted(chdir):
    runner.invoke(app, ["init"])
    _write_scheme_unordered(chdir / "scholia" / "scheme.yaml")
    result = runner.invoke(app, ["update"])
    assert result.exit_code == 0
    header = (chdir / "scholia" / "students.csv").read_text().splitlines()[0]
    assert header == "student_id,q1,q2,note"
    assert "Updated headers" in result.output


def test_update_syncs_headers_preserve_order(chdir):
    runner.invoke(app, ["init"])
    _write_scheme_unordered(chdir / "scholia" / "scheme.yaml")
    result = runner.invoke(app, ["update", "--preserve-order"])
    assert result.exit_code == 0
    header = (chdir / "scholia" / "students.csv").read_text().splitlines()[0]
    assert header == "student_id,q2,q1,note"


def test_init_custom_directory(chdir):
    result = runner.invoke(app, ["init", "my-exam"])
    assert result.exit_code == 0
    assert (chdir / "my-exam" / "scheme.yaml").exists()
    assert (chdir / "my-exam" / "students.csv").exists()
    assert "my-exam" in result.output


def test_update_custom_directory(chdir, scheme_data):
    runner.invoke(app, ["init", "my-exam"])
    _write_scheme(chdir / "my-exam" / "scheme.yaml", scheme_data)
    result = runner.invoke(app, ["update", "--dir", "my-exam"])
    assert result.exit_code == 0
    header = (chdir / "my-exam" / "students.csv").read_text().splitlines()[0]
    assert "q1(a)" in header


def test_mark_custom_directory(chdir, scheme_data):
    runner.invoke(app, ["init", "my-exam"])
    _write_scheme(chdir / "my-exam" / "scheme.yaml", scheme_data)
    _write_students(
        chdir / "my-exam" / "students.csv",
        [{"student_id": "s001", "q1(a)": "b", "q1(b)": "b"}],
    )
    result = runner.invoke(app, ["mark", "--dir", "my-exam"])
    assert result.exit_code == 0
    assert (chdir / "my-exam" / "feedback" / "s001.md").exists()
    assert (chdir / "my-exam" / "summary.md").exists()


def test_mark_generates_output(chdir, scheme_data):
    runner.invoke(app, ["init"])
    _write_scheme(chdir / "scholia" / "scheme.yaml", scheme_data)
    _write_students(
        chdir / "scholia" / "students.csv",
        [{"student_id": "s001", "q1(a)": "b", "q1(b)": "b"}],
    )
    result = runner.invoke(app, ["mark"])
    assert result.exit_code == 0
    assert (chdir / "scholia" / "feedback" / "s001.md").exists()
    assert (chdir / "scholia" / "summary.md").exists()
    assert "Generated feedback" in result.output
    assert "Generated summary" in result.output
