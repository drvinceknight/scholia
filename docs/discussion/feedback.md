# Feedback

Scholia generates per-student feedback as plain markdown files. This
page discusses the design decisions behind this choice.

**Plain markdown.** Markdown is the most portable format for structured
text: it renders neatly in GitHub, Jupyter, most email clients, and every
major documentation platform. Students can open a `.md` file in any text
editor without any tooling. PDF is not produced by default, because PDF
generation requires a render pipeline; the markdown source is the
artefact, and instructors or institutions can convert it as needed.

**Category feedback, not student-specific prose.** The feedback string
for a category is written once in the scheme and appears verbatim in every
student's file who received that category. This is a deliberate trade-off.
Writing individualised prose for every student is time-consuming and
inconsistent: the same error is described differently in the twentieth
script than in the first. Category feedback is consistent by construction.

Notably, this does not prevent personalisation. An instructor who wants
to add a student-specific note can edit the generated markdown file
directly after running `scholia mark`. The generated file is a starting
point, not a final document.

**Incomplete students.** A feedback file is generated for every student
in the roster, even those who have not been fully marked. Incomplete
questions appear as "not yet marked", and the total is shown as
"incomplete". This means partial feedback can be shared during a long
marking period, and students who have been missed are easily spotted.

**The marks CSV.** `marks.csv` contains one row per student with their
total mark. It is intended for upload to an external grade book or
spreadsheet. Students who have not been fully marked appear with an
empty total.

**The summary file.** `summary.md` gives a cohort-level view: mean,
median, standard deviation, minimum, and maximum total, together with a
breakdown of how many students received each category for each question.
This breakdown is often more informative than the mark distribution alone,
because it shows where the cohort clustered in the scheme: which
categories were common, which were rare, and which questions produced the
most variation. The summary charts complement this with a visual overview.
