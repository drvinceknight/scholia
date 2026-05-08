# Write a scheme

The scheme lives in `scholia/scheme.yaml`. Edit it directly with any
text editor. The format is a YAML mapping: top-level keys are question
names, and each question maps category labels to a mark and a feedback
string.

## Basic structure

```yaml
q1(a):
  a:
    marks: 0
    feedback: "Did not attempt the question."
  b:
    marks: 8
    feedback: "Correct and well-presented solution."
  c:
    marks: 6
    feedback: "Correct method but the final calculation contains an error."
```

Question names can be any string (`q1`, `q1(a)`, `part_2`, etc.).
Category labels are single characters by convention but can be any
short string. Marks are integers.

## Adding a new question

Append a new top-level key to the file:

```yaml
q2:
  a:
    marks: 0
    feedback: "No working shown."
  b:
    marks: 5
    feedback: "Full marks."
```

## Adding a new category mid-marking

If a student's work does not fit any existing category, add a new one
to the scheme:

```yaml
q1(a):
  d:
    marks: 4
    feedback: "Attempted but the method is incorrect."
```

Run `scholia mark` to regenerate all feedback. Any student subsequently
assigned to category `d` will receive the new mark and feedback string;
previously assigned students are unaffected until their assignment is
updated.

## Syncing the student roster

After adding a new question to the scheme, run:

```bash
scholia update
```

This adds the new question column to `students.csv` so that it is ready
to receive category labels. See
[Sync scheme headers](update-a-student.md) for details.

## Adjusting marks

A category's mark can be changed at any time by editing the `marks`
field and re-running `scholia mark`. All feedback files and the summary
are regenerated from the updated scheme. See the
[discussion on the marking approach](../discussion/marking-approach.md)
for the rationale behind this design.
