"""Marking scheme: criteria and their scored categories."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

SCHEME_FILENAME: str = "scheme.yaml"


@dataclass
class Band:
    """A named grade band defined by an inclusive lower threshold."""

    name: str
    min: int


@dataclass
class Category:
    """A single scored outcome for one criterion."""

    marks: int
    feedback: str


@dataclass
class Criterion:
    """A criterion in the marking scheme, with its possible categories."""

    categories: dict[str, Category] = field(default_factory=dict)


@dataclass
class Scheme:
    """The full marking scheme for one piece of assessment."""

    criteria: dict[str, Criterion] = field(default_factory=dict)
    bands: list[Band] = field(default_factory=list)

    @classmethod
    def load(cls, path: Path) -> Scheme:
        """Load a scheme from a YAML file."""
        with open(path) as file_handle:
            raw: dict[str, Any] = yaml.safe_load(file_handle) or {}
        bands_data = raw.pop("bands", None) or []
        bands = [Band(name=b["name"], min=b["min"]) for b in bands_data]
        criteria: dict[str, Criterion] = {}
        for criterion_name, categories_data in raw.items():
            categories: dict[str, Category] = {}
            for category_id, category_data in (categories_data or {}).items():
                categories[category_id] = Category(
                    marks=category_data["marks"],
                    feedback=category_data["feedback"],
                )
            criteria[criterion_name] = Criterion(categories=categories)
        return cls(criteria=criteria, bands=bands)

    def save(self, path: Path) -> None:
        """Write the scheme to a YAML file."""
        raw: dict[str, Any] = {}
        if self.bands:
            raw["bands"] = [{"name": b.name, "min": b.min} for b in self.bands]
        for criterion_name, criterion in self.criteria.items():
            raw[criterion_name] = {}
            for category_id, category in criterion.categories.items():
                raw[criterion_name][category_id] = {
                    "marks": category.marks,
                    "feedback": category.feedback,
                }
        with open(path, "w") as file_handle:
            yaml.dump(
                raw,
                file_handle,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
            )

    def criterion_names(self) -> list[str]:
        """Return criterion names in definition order."""
        return list(self.criteria.keys())

    def get_category(self, criterion_name: str, category_id: str) -> Category | None:
        """Return the category, or ``None`` if not found."""
        criterion = self.criteria.get(criterion_name)
        if criterion is None:
            return None
        return criterion.categories.get(category_id)
