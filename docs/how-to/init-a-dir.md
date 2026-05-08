# Initialise a directory

Run the following from the directory where you want to keep your
marking:

```bash
scholia init
```

This creates a `scholia/` subdirectory containing two files:

- `scheme.yaml`: an empty marking scheme, ready to be edited.
- `students.csv`: a roster with only the header row `student_id`.

If either file already exists, scholia skips it and reports this in the
output. It is therefore safe to re-run `scholia init` without
overwriting work in progress.

The full directory layout after initialisation is:

```
scholia/
    scheme.yaml
    students.csv
```

The `feedback/` subdirectory, `marks.csv`, `summary.md`, and `charts/`
are created later when `scholia mark` is run.
