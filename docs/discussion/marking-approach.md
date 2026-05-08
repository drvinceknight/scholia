# Marking approach

Scholia is built around a single observation: marking a cohort does not
mean assigning arbitrary numbers. Markers assign *outcomes*. A student
either attempted the question or did not; they either demonstrated the
key technique or applied it incorrectly; they either reached the correct
answer or made a specific error. These outcomes repeat across the cohort,
and the mark is a consequence of the outcome, not an independent
judgement.

**Category-based marking.** Scholia expresses this directly. The marking
scheme defines a finite set of categories for each question; each category
has a mark and a feedback string. When marking a student, the marker
decides which category their response falls into and records that label.
The numeric mark is derived from the scheme, not entered directly.

**Post-hoc adjustment.** This separation has a practical benefit: marks
can be adjusted after the fact without re-reading any student's work. If,
having marked 30 scripts, category `c` in `q1(a)` should be worth 5 marks
rather than 6 (because the initial judgement was too lenient, or to fit
an expected grade profile), editing one line in `scheme.yaml` and
re-running `scholia mark` is sufficient. All feedback and statistics are
regenerated consistently. No student record needs editing.

**Adding categories mid-marking.** Similarly, if a student's response
does not fit any existing category, a new one is added to the scheme
rather than forcing a fit. This keeps the scheme honest and allows
precise feedback for edge cases, while keeping the most common outcomes
grouped.

**Numeric marks as a summary.** Scholia treats numeric marks as a
summary statistic derived from qualitative judgements, rather than as
the primary object. The feedback text, not the number, is the main
output. The total mark appears in the feedback file for the student's
reference, and in the cohort summary for analysis.

This approach is closely related to *rubric-based marking* as discussed
in the educational assessment literature. Panadero and Jonsson (2013)
review how scoring rubrics support formative assessment, noting that
separating qualitative judgement from numeric scoring improves
consistency and the quality of feedback returned to students. The
earlier review by Jonsson and Svingby (2007) reaches similar conclusions
and is now a standard reference on rubric reliability and validity.
Scholia provides a lightweight implementation of the same principle,
suited to the kind of written assessment common in mathematics and
related disciplines, where a small number of distinct error types
account for most of the variation in student responses.

## References

Jonsson, A. and Svingby, G. (2007). The use of scoring rubrics:
Reliability, validity and educational consequences. *Educational
Research Review*, 2(2), 130–144.

Panadero, E. and Jonsson, A. (2013). The use of scoring rubrics for
formative assessment purposes revisited: A review. *Educational
Research Review*, 9, 129–144.
