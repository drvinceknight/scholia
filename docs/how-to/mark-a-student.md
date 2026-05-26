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

## Adding a note

The `note` column holds free-form text that is appended to a student's
feedback file under a `## Note` heading. Use it to record anything that
does not fit neatly into a category: a late-submission penalty, a
comment on an unusual approach, or a reminder to follow up.

```csv
student_id,q1(a),q1(b),note
s001,b,b,
s002,c,a,"Good attempt, but the final step was missing."
```

A note can contain commas, apostrophes, and other punctuation without
any manual quoting; a spreadsheet application or Python's `csv` module
handles the escaping automatically.

Leave the cell empty for students who need no note. The `## Note`
section is omitted from their feedback file entirely.
