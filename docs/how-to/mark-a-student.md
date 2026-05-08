# Mark a student

Record category labels for students by editing
`scholia/students.csv` directly. Each row is one student; each
question column holds the category label assigned to that student.

```csv
student_id,q1(a),q1(b)
s001,b,b
s002,c,a
```

A spreadsheet application or any text editor works well. Fill in
category labels as you mark, leaving a cell empty if a student has not
yet been marked for that question.

Empty cells are treated as unassigned. Any student with at least one
empty cell will show an incomplete total in their feedback file and
will be excluded from the cohort statistics in `summary.md`.

## Adding students

Append a new row for each student with a unique `student_id`. The
question columns can be left empty initially and filled in as marking
progresses.

## Correcting an assignment

Edit the relevant cell directly. After saving the CSV, re-run
`scholia mark` to regenerate feedback with the corrected category.
