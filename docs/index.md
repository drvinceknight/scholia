# scholia

<p align="center">
  <span style="display:inline-block; background:#1e2a4a; padding:20px 28px; border-radius:16px;">
    <img src="img/logo.svg" width="72">
  </span>
</p>

<p align="center"><em>Category-based marking with Python.</em></p>

---

Marking a cohort by hand couples two separate activities: the qualitative
judgement of what a student did, and the numerical decision of how many
marks that deserves. Once combined in a single number, any later
adjustment requires re-reading scripts and overwriting records across the
whole cohort. This is tedious and inconsistent.

Scholia separates the two. Instead of recording a mark directly, you
assign a short category label (such as `b` or `c`) for each question.
Marks and feedback text are defined once in a YAML scheme file. To adjust
a mark, edit one line in the scheme and re-run `scholia mark`. Feedback
for the entire cohort is regenerated automatically.

## What scholia produces

Scholia organises a piece of assessment into a collection of artefacts, all stored
in a `scholia/` directory:

- **`scheme.yaml`**: the marking scheme. For each question, a set of
  labelled categories, each with a numeric mark and a feedback string.
- **`students.csv`**: the student roster. One row per student, with a
  column for each question holding the assigned category label.
- **`scholia/marks.csv`**: a flat CSV of student IDs and total marks,
  ready to upload to a grade book.
- **`scholia/feedback/`**: per-student markdown feedback files, generated
  from the scheme and the assignments.
- **`scholia/summary.md`**: cohort statistics and a set of charts.

## Installation

```bash
uv add scholia
```

Or with pip:

```bash
python -m pip install scholia
```

## Quick start

```bash
scholia init
# edit scholia/scheme.yaml
scholia update
# edit scholia/students.csv to fill in category labels
scholia mark
```

See the [Tutorial](tutorial/index.md) for a full walkthrough.
