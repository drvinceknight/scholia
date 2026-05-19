# Why am I getting `CategoryNotInSchemeError`?

`CategoryNotInSchemeError` is raised when `scholia` finds a non-empty
category label in `students.csv` that has no matching entry in the
corresponding question in `scheme.yaml`. In other words, a student has
been assigned a category that the scheme does not recognise.

**What the error tells you.** The exception message includes the
student identifier, the question name, the unrecognised category label,
and the list of valid labels that are defined for that question. For
example:

```
CategoryNotInSchemeError: Student 's007' has category 'd' for question
'q1(a)', which is not defined in the scheme. Valid categories are:
['a', 'b', 'c'].
```

**Common causes.**

- A typo in `students.csv`. Category labels are case-sensitive, so `B`
  and `b` are different. Check that the label in the CSV matches the
  label in `scheme.yaml` exactly.
- A category was renamed or removed from `scheme.yaml` after some
  students had already been assigned to it. Re-run `scholia update` to
  sync the headers, then correct the affected cells.
- A new category was added to `students.csv` before it was added to
  `scheme.yaml`. Add the category to the scheme first, or leave the
  cell blank until the scheme is ready.

**How to fix it.** Open `students.csv` and find the row for the
student named in the error. Locate the column for the question named in
the error. Either correct the label to one of the valid categories
listed in the error message, or clear the cell to leave the question
unassigned (an empty cell is treated as not yet marked and does not
raise an error).

**Why scholia raises an error rather than ignoring the label.** An
unrecognised category is almost always a mistake. Silently treating it
as "not yet marked" would hide the problem: the student would appear
incomplete in the summary and receive no marks for that question, with
no indication that something was wrong. Raising an error immediately
makes the problem visible and prevents incorrect marks and feedback from
being generated.
