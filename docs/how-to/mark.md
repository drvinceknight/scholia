# Generate marks and feedback

Once category labels have been filled in for at least some students,
generate feedback and summary statistics:

```bash
scholia mark
```

Scholia reads `scholia/scheme.yaml` and `scholia/students.csv`, then
writes:

- **`scholia/feedback/<student_id>.md`** for each student in the roster.
- **`scholia/marks.csv`** with student IDs and total marks.
- **`scholia/summary.md`** with cohort-level statistics.
- **`scholia/charts/`**: a set of summary charts.

`scholia mark` can be run as many times as needed. Each run overwrites
the previous output, so you can adjust the scheme or student
assignments and regenerate freely.

## Partial marking

There is no need to have assigned every student and question before
running `scholia mark`. Students with incomplete assignments receive a
feedback file that reports each unassigned question as "not yet marked",
and their total is shown as "incomplete". They are excluded from the
cohort statistics. This allows you to check the summary as you go, and
catch scheme issues early.
