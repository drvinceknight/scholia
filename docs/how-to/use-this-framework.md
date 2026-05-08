# Use the Python API

Scholia exposes its core functions as a Python library, making it
straightforward to integrate into scripts, notebooks, or other tooling.

## Loading the scheme and roster

```python
from pathlib import Path
import scholia

scheme = scholia.Scheme.load(Path("scholia/scheme.yaml"))
students = scholia.Students.load(Path("scholia/students.csv"))
```

## Computing marks

```python
for student in students.students:
    total = scholia.compute_total_marks(student, scheme)
    print(student.student_id, total)
```

`scholia.compute_question_marks` returns a dictionary mapping each
question name to its numeric mark (or `None` if the student has no
valid category assigned). `scholia.compute_total_marks` sums these,
returning `None` if any question is incomplete.

## Generating feedback programmatically

```python
from pathlib import Path
import scholia

scholia.generate_all_feedback(students, scheme, Path("scholia/feedback"))
```

## Generating the marks CSV

```python
from pathlib import Path
import scholia

scholia.generate_marks_csv(students, scheme, Path("scholia/marks.csv"))
```

## Generating the summary

```python
from pathlib import Path
import scholia

scholia.generate_summary(
    students,
    scheme,
    Path("scholia/summary.md"),
    charts_dir=Path("scholia/charts"),
)
```

Passing `charts_dir=None` skips chart generation and produces a
text-only summary.

## Updating a student from a script

```python
students.update("s001", "q1(a)", "b")
students.save(Path("scholia/students.csv"))
```

The `update` method raises `ValueError` if the student ID is not in the
roster.
