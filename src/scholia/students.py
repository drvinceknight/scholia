"""Student roster and per-student category assignments."""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass, field
from pathlib import Path

STUDENTS_FILENAME: str = "students.csv"


@dataclass
class Student:
    """A single student and their category assignments."""

    student_id: str
    assignments: dict[str, str] = field(default_factory=dict)
    note: str = ""


@dataclass
class Students:
    """The full student roster."""

    students: list[Student] = field(default_factory=list)
    question_names: list[str] = field(default_factory=list)

    @classmethod
    def load(cls, path: Path) -> Students:
        """Load the roster from a CSV file.

        UTF-8 (with or without BOM) is tried first. For files in a
        legacy single-byte encoding (e.g. Mac Roman or Windows-1252
        exported by some university systems), ``charset-normalizer``
        detects the encoding; if detection fails or the detected
        encoding cannot decode the raw bytes, Mac Roman is used as a
        final fallback.
        """
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            from charset_normalizer import from_bytes as _from_bytes

            best = _from_bytes(raw).best()
            if best is not None:
                try:
                    text = raw.decode(best.encoding)
                except (UnicodeDecodeError, LookupError):
                    text = raw.decode("mac_roman")
            else:
                text = raw.decode("mac_roman")
        reader = csv.DictReader(io.StringIO(text))
        fieldnames = list(reader.fieldnames or [])
        question_names = [
            f for f in fieldnames if f not in ("student_id", "note")
        ]
        students: list[Student] = []
        for row in reader:
            assignments = {
                question: row.get(question, "") for question in question_names
            }
            students.append(
                Student(
                    student_id=row["student_id"],
                    assignments=assignments,
                    note=row.get("note", ""),
                )
            )
        return cls(students=students, question_names=question_names)

    def save(self, path: Path) -> None:
        """Write the roster to a CSV file."""
        fieldnames = ["student_id"] + self.question_names + ["note"]
        with open(path, "w", newline="") as file_handle:
            writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
            writer.writeheader()
            for student in self.students:
                row: dict[str, str] = {"student_id": student.student_id}
                for question in self.question_names:
                    row[question] = student.assignments.get(question, "")
                row["note"] = student.note
                writer.writerow(row)

    def sync_headers(self, question_names: list[str]) -> None:
        """Sync question columns with the given list.

        Questions not yet in the roster are added with empty values.
        The column order is updated to match ``question_names``; columns
        already present but absent from ``question_names`` are appended
        at the end.
        """
        extra = [q for q in self.question_names if q not in question_names]
        new_order = list(question_names) + extra
        for student in self.students:
            for question in new_order:
                if question not in student.assignments:
                    student.assignments[question] = ""
        self.question_names = new_order

    def update(self, student_id: str, question: str, category: str) -> None:
        """Set a student's category for one question.

        If ``question`` is not yet a column in the roster, it is added.

        Raises:
            ValueError: If ``student_id`` is not in the roster.
        """
        for student in self.students:
            if student.student_id == student_id:
                if question not in self.question_names:
                    self.question_names.append(question)
                student.assignments[question] = category
                return
        raise ValueError(f"Student {student_id!r} not found")

    def get_student(self, student_id: str) -> Student | None:
        """Return the student with the given ID, or ``None``."""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
