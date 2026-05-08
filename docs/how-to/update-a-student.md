# Sync scheme headers

After editing `scholia/scheme.yaml`, run:

```bash
scholia update
```

This reads the question names from the scheme and updates the column
headers in `scholia/students.csv` to match. By default the questions
are sorted alphabetically. To keep the order they appear in
`scheme.yaml` instead, pass the `--preserve-order` flag:

```bash
scholia update --preserve-order
```

Any question already in the CSV retains its data. Questions present in
the CSV but absent from the scheme are appended after the scheme
questions rather than removed, so no data is lost.

Typically, run `scholia update` once after the initial scheme is
written, and again whenever a new question is added to the scheme.
