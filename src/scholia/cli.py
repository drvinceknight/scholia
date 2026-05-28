"""Command-line interface for scholia."""

from __future__ import annotations

from pathlib import Path

import typer

from scholia.feedback import generate_all_feedback
from scholia.scheme import SCHEME_FILENAME, Scheme
from scholia.stats import generate_marks_csv, generate_summary
from scholia.students import STUDENTS_FILENAME, Students

app = typer.Typer(help="Scholia: a marking aid library.")

_DEFAULT_DIR: str = "scholia"
_INITIAL_STUDENTS_CONTENT: str = "student_id\n"


@app.command()
def init(
    directory: str = typer.Argument(
        _DEFAULT_DIR, help="Name of the directory to create."
    ),
) -> None:
    """Initialise a marking directory with scheme.yaml and students.csv."""
    scholia_dir = Path(directory)
    scholia_dir.mkdir(exist_ok=True)

    scheme_path = scholia_dir / SCHEME_FILENAME
    if not scheme_path.exists():
        Scheme().save(scheme_path)
        typer.echo(f"Created {scheme_path.as_posix()}")
    else:
        typer.echo(f"{scheme_path.as_posix()} already exists, skipping.")

    students_path = scholia_dir / STUDENTS_FILENAME
    if not students_path.exists():
        students_path.write_text(_INITIAL_STUDENTS_CONTENT)
        typer.echo(f"Created {students_path.as_posix()}")
    else:
        typer.echo(f"{students_path.as_posix()} already exists, skipping.")


@app.command()
def update(
    preserve_order: bool = typer.Option(
        False,
        "--preserve-order",
        help="Keep criterion order from scheme.yaml instead of sorting alphabetically.",
    ),
    directory: str = typer.Option(
        _DEFAULT_DIR, "--dir", help="Marking directory to operate on."
    ),
) -> None:
    """Sync criterion headers in students.csv from scheme.yaml."""
    scholia_dir = Path(directory)
    scheme_path = scholia_dir / SCHEME_FILENAME
    students_path = scholia_dir / STUDENTS_FILENAME

    scheme = Scheme.load(scheme_path)
    students = Students.load(students_path)

    criterion_names = scheme.criterion_names()
    if not preserve_order:
        criterion_names = sorted(criterion_names)

    students.sync_headers(criterion_names)
    students.save(students_path)
    typer.echo(f"Updated headers in {students_path.as_posix()}")


@app.command()
def mark(
    directory: str = typer.Option(
        _DEFAULT_DIR, "--dir", help="Marking directory to operate on."
    ),
) -> None:
    """Generate summary statistics and individual feedback files."""
    scholia_dir = Path(directory)
    scheme_path = scholia_dir / SCHEME_FILENAME
    students_path = scholia_dir / STUDENTS_FILENAME

    scheme = Scheme.load(scheme_path)
    students = Students.load(students_path)

    feedback_dir = scholia_dir / "feedback"
    generate_all_feedback(students, scheme, feedback_dir)
    typer.echo(f"Generated feedback in {feedback_dir.as_posix()}/")

    marks_csv_path = scholia_dir / "marks.csv"
    generate_marks_csv(students, scheme, marks_csv_path)
    typer.echo(f"Generated marks at {marks_csv_path.as_posix()}")

    summary_path = scholia_dir / "summary.md"
    assets_dir = scholia_dir / "assets"
    generate_summary(students, scheme, summary_path, assets_dir)
    typer.echo(f"Generated summary at {summary_path.as_posix()}")
