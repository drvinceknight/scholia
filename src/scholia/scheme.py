"""Marking scheme: questions and their scored categories."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

SCHEME_FILENAME: str = "scheme.yaml"


@dataclass
class Category:
    """A single scored outcome for one question."""

    marks: int
    feedback: str


@dataclass
class Question:
    """A question in the marking scheme, with its possible categories."""

    categories: dict[str, Category] = field(default_factory=dict)


@dataclass
class Scheme:
    """The full marking scheme for one piece of assessment."""

    questions: dict[str, Question] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> Scheme:
        """Load a scheme from a YAML file."""
        with open(path) as file_handle:
            raw: dict[str, Any] = yaml.safe_load(file_handle) or {}
        questions: dict[str, Question] = {}
        for question_name, categories_data in raw.items():
            categories: dict[str, Category] = {}
            for category_id, category_data in (categories_data or {}).items():
                categories[category_id] = Category(
                    marks=category_data["marks"],
                    feedback=category_data["feedback"],
                )
            questions[question_name] = Question(categories=categories)
        return cls(questions=questions)

    def save(self, path: Path) -> None:
        """Write the scheme to a YAML file."""
        raw: dict[str, Any] = {}
        for question_name, question in self.questions.items():
            raw[question_name] = {}
            for category_id, category in question.categories.items():
                raw[question_name][category_id] = {
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

    def question_names(self) -> list[str]:
        """Return question names in definition order."""
        return list(self.questions.keys())

    def get_category(self, question_name: str, category_id: str) -> Category | None:
        """Return the category, or ``None`` if not found."""
        question = self.questions.get(question_name)
        if question is None:
            return None
        return question.categories.get(category_id)
