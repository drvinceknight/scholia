# scholia

<img src="docs/img/logo.svg" width="80" align="right">

Scholia is a category-based marking aid library for Python. Rather than
recording a raw numeric mark per student and question, we record a
_category label_ that maps to both a mark and a prose feedback string
defined in the marking scheme. Adjusting a mark mid-cohort means editing
one line in the scheme; all feedback is regenerated automatically.

## Installation

```bash
uv add scholia
```

## Quick start

```bash
scholia init
# edit scholia/scheme.yaml
scholia update
# edit scholia/students.csv to fill in category labels
scholia mark
```

## Documentation

Full documentation is available at the project site.

## Development

Scholia uses [uv](https://docs.astral.sh/uv/) for dependency management,
[ruff](https://docs.astral.sh/ruff/) for formatting and linting,
[ty](https://docs.astral.sh/ty/) for type checking, and
[pytest](https://docs.pytest.org/) for testing.

```bash
uv sync --all-groups
uv run pytest
uv run ruff format .
uv run ruff check .
uv run ty check src/scholia
```
