# Initialise a named directory

By default, `scholia init` creates a subdirectory called `scholia/`.
Pass a name to create a differently-named directory instead:

```bash
scholia init coursework-1
```

This creates `coursework-1/scheme.yaml` and `coursework-1/students.csv`,
exactly as the default initialisation would.

To run subsequent commands against a non-default directory, pass
`--dir`:

```bash
scholia update --dir coursework-1
scholia mark --dir coursework-1
```

This makes it straightforward to keep multiple pieces of assessment in
the same folder:

```
my-course/
    coursework-1/
        scheme.yaml
        students.csv
        marks.csv
        summary.md
        feedback/
        charts/
    exam-2025/
        scheme.yaml
        students.csv
        marks.csv
        summary.md
        feedback/
        charts/
```
