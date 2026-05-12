"""Generate summary statistics and charts for a marked cohort."""

from __future__ import annotations

import csv
import statistics
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from scholia.marks import compute_question_marks, compute_total_marks
from scholia.scheme import Scheme
from scholia.students import Students


def _generate_distribution_chart(all_totals: list[int], charts_dir: Path) -> list[str]:
    fig, ax = plt.subplots()
    ax.hist(all_totals, bins="auto", edgecolor="black")
    ax.set_xlabel("Total marks")
    ax.set_ylabel("Number of students")
    ax.set_title("Mark distribution")
    fig.savefig(charts_dir / "distribution.png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    return [
        "## Mark distribution",
        "",
        "![Mark distribution](charts/distribution.png)",
        "",
    ]


def _generate_cumulative_chart(all_totals: list[int], charts_dir: Path) -> list[str]:
    sorted_totals = sorted(all_totals)
    num_students = len(sorted_totals)
    proportions = [(idx + 1) / num_students for idx in range(num_students)]
    fig, ax = plt.subplots()
    ax.step(sorted_totals, proportions, where="post")
    ax.set_xlabel("Total marks")
    ax.set_ylabel("Proportion of students")
    ax.set_ylim(0, 1.05)
    ax.set_title("Cumulative mark distribution")
    fig.savefig(charts_dir / "cumulative.png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    return [
        "## Cumulative mark distribution",
        "",
        "![Cumulative mark distribution](charts/cumulative.png)",
        "",
    ]


def _generate_boxplot_chart(
    per_question_mark_values: dict[str, list[int]], charts_dir: Path
) -> list[str]:
    question_names = list(per_question_mark_values.keys())
    data = [per_question_mark_values[q] for q in question_names]
    fig, ax = plt.subplots(figsize=(max(4, len(question_names) * 1.5), 3))
    ax.boxplot(data, tick_labels=question_names)
    ax.set_ylabel("Marks")
    ax.set_title("Marks per question")
    fig.savefig(charts_dir / "boxplot.png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    return [
        "## Marks per question",
        "",
        "![Marks per question](charts/boxplot.png)",
        "",
    ]


def _generate_correlation_chart(
    question_names: list[str],
    complete_mark_rows: list[list[int]],
    charts_dir: Path,
) -> list[str]:
    data = np.array(complete_mark_rows, dtype=float).T
    corr_matrix = np.corrcoef(data)
    num_questions = len(question_names)
    fig_size = max(4, num_questions)
    fig, ax = plt.subplots(figsize=(fig_size, fig_size))
    image = ax.imshow(corr_matrix, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set_xticks(range(num_questions))
    ax.set_yticks(range(num_questions))
    ax.set_xticklabels(question_names, rotation=45, ha="right")
    ax.set_yticklabels(question_names)
    for row_idx in range(num_questions):
        for col_idx in range(num_questions):
            value = corr_matrix[row_idx, col_idx]
            label = f"{value:.2f}" if not np.isnan(value) else "N/A"
            ax.text(col_idx, row_idx, label, ha="center", va="center", fontsize=9)
    plt.colorbar(image, ax=ax)
    ax.set_title("Question mark correlations")
    fig.tight_layout()
    fig.savefig(charts_dir / "correlation.png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    return [
        "## Question mark correlations",
        "",
        "![Question mark correlations](charts/correlation.png)",
        "",
    ]


def _generate_charts(
    all_totals: list[int],
    per_question_mark_values: dict[str, list[int]],
    question_names: list[str],
    complete_mark_rows: list[list[int]],
    charts_dir: Path,
) -> list[str]:
    charts_dir.mkdir(parents=True, exist_ok=True)
    lines = _generate_distribution_chart(all_totals, charts_dir)
    if len(all_totals) >= 2:
        lines += _generate_cumulative_chart(all_totals, charts_dir)
        lines += _generate_boxplot_chart(per_question_mark_values, charts_dir)
        if len(question_names) >= 2:
            lines += _generate_correlation_chart(
                question_names, complete_mark_rows, charts_dir
            )
    return lines


def generate_summary(
    students: Students,
    scheme: Scheme,
    output_path: Path,
    charts_dir: Path | None = None,
) -> None:
    """Write a cohort summary to ``output_path``.

    When ``charts_dir`` is provided, saves a distribution histogram,
    cumulative distribution, per-question boxplot, and (with at least two
    questions and two complete students) a correlation heatmap.
    """
    scheme_question_names = scheme.question_names()
    all_totals: list[int] = []
    per_question_categories: dict[str, dict[str, int]] = {
        q: {} for q in scheme_question_names
    }
    per_question_mark_values: dict[str, list[int]] = {
        q: [] for q in scheme_question_names
    }
    complete_mark_rows: list[list[int]] = []

    for student in students.students:
        total = compute_total_marks(student, scheme)
        question_marks = compute_question_marks(student, scheme)

        if total is not None:
            all_totals.append(total)
            complete_mark_rows.append(
                [
                    m
                    for q in scheme_question_names
                    if (m := question_marks[q]) is not None
                ]
            )

        for question_name in scheme_question_names:
            category_id = student.assignments.get(question_name, "")
            if category_id:
                counter = per_question_categories[question_name]
                counter[category_id] = counter.get(category_id, 0) + 1
            marks = question_marks.get(question_name)
            if marks is not None:
                per_question_mark_values[question_name].append(marks)

    lines: list[str] = ["# Marking summary", ""]

    if all_totals:
        mean = statistics.mean(all_totals)
        median = statistics.median(all_totals)
        std = statistics.stdev(all_totals) if len(all_totals) > 1 else 0.0
        lines += [
            f"**Students marked:** {len(all_totals)}",
            "",
            f"**Mean:** {mean:.2f}",
            "",
            f"**Median:** {median:.2f}",
            "",
            f"**Standard deviation:** {std:.2f}",
            "",
            f"**Min:** {min(all_totals)}",
            "",
            f"**Max:** {max(all_totals)}",
            "",
        ]
        if charts_dir is not None:
            lines += _generate_charts(
                all_totals,
                per_question_mark_values,
                scheme_question_names,
                complete_mark_rows,
                charts_dir,
            )
    else:
        lines += ["No complete marks yet.", ""]

    lines += ["## Per-question breakdown", ""]

    for question_name, category_counts in per_question_categories.items():
        question = scheme.questions[question_name]
        lines += [f"### {question_name}", ""]
        for category_id, category in question.categories.items():
            count = category_counts.get(category_id, 0)
            label = category.feedback.removesuffix(".")
            lines.append(f"- {label}: {count} student(s) ({category.marks} marks)")
        lines.append("")

    output_path.write_text("\n".join(lines))


def generate_marks_csv(
    students: Students,
    scheme: Scheme,
    output_path: Path,
) -> None:
    """Write student IDs and total marks to a CSV file.

    Students with incomplete marking have an empty ``total_marks`` cell.
    """
    with open(output_path, "w", newline="") as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow(["student_id", "total_marks"])
        for student in students.students:
            total = compute_total_marks(student, scheme)
            writer.writerow([student.student_id, "" if total is None else total])
