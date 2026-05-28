"""Generate summary statistics and charts for a marked cohort."""

from __future__ import annotations

import csv
import statistics
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from scholia.marks import compute_criterion_marks, compute_total_marks
from scholia.scheme import Band, Scheme
from scholia.students import Students


def _draw_band_lines(ax: plt.Axes, bands: list[Band]) -> None:
    for band in bands[1:]:
        ax.axvline(band.min, color="black", linestyle="--", linewidth=1, alpha=0.7)
        ax.text(
            band.min,
            0.97,
            band.name,
            transform=ax.get_xaxis_transform(),
            ha="left",
            va="top",
            fontsize=8,
            rotation=90,
        )


def _generate_distribution_chart(
    all_totals: list[int], charts_dir: Path, bands: list[Band] | None = None
) -> list[str]:
    fig, ax = plt.subplots()
    ax.hist(all_totals, bins="auto", edgecolor="black")
    ax.set_xlabel("Total marks")
    ax.set_ylabel("Number of students")
    ax.set_title("Mark distribution")
    if bands:
        _draw_band_lines(ax, bands)
    fig.savefig(charts_dir / "distribution.png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    return [
        "## Mark distribution",
        "",
        "![Mark distribution](assets/distribution.png)",
        "",
    ]


def _generate_cumulative_chart(
    all_totals: list[int], charts_dir: Path, bands: list[Band] | None = None
) -> list[str]:
    sorted_totals = sorted(all_totals)
    num_students = len(sorted_totals)
    proportions = [(idx + 1) / num_students for idx in range(num_students)]
    fig, ax = plt.subplots()
    ax.step(sorted_totals, proportions, where="post")
    ax.set_xlabel("Total marks")
    ax.set_ylabel("Proportion of students")
    ax.set_ylim(0, 1.05)
    ax.set_title("Cumulative mark distribution")
    if bands:
        _draw_band_lines(ax, bands)
    fig.savefig(charts_dir / "cumulative.png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    return [
        "## Cumulative mark distribution",
        "",
        "![Cumulative mark distribution](assets/cumulative.png)",
        "",
    ]


def _generate_boxplot_chart(
    per_criterion_mark_values: dict[str, list[int]], charts_dir: Path
) -> list[str]:
    criterion_names = list(per_criterion_mark_values.keys())
    data = [per_criterion_mark_values[q] for q in criterion_names]
    fig, ax = plt.subplots(figsize=(max(4, len(criterion_names) * 1.5), 3))
    ax.boxplot(data, tick_labels=criterion_names)
    ax.set_ylabel("Marks")
    ax.set_title("Marks per criterion")
    fig.savefig(charts_dir / "boxplot.png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    return [
        "## Marks per criterion",
        "",
        "![Marks per criterion](assets/boxplot.png)",
        "",
    ]


def _generate_correlation_chart(
    criterion_names: list[str],
    complete_mark_rows: list[list[int]],
    charts_dir: Path,
) -> list[str]:
    data = np.array(complete_mark_rows, dtype=float).T
    corr_matrix = np.corrcoef(data)
    num_criteria = len(criterion_names)
    fig_size = max(4, num_criteria)
    fig, ax = plt.subplots(figsize=(fig_size, fig_size))
    image = ax.imshow(corr_matrix, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set_xticks(range(num_criteria))
    ax.set_yticks(range(num_criteria))
    ax.set_xticklabels(criterion_names, rotation=45, ha="right")
    ax.set_yticklabels(criterion_names)
    for row_idx in range(num_criteria):
        for col_idx in range(num_criteria):
            value = corr_matrix[row_idx, col_idx]
            label = f"{value:.2f}" if not np.isnan(value) else "N/A"
            ax.text(col_idx, row_idx, label, ha="center", va="center", fontsize=9)
    plt.colorbar(image, ax=ax)
    ax.set_title("Criterion mark correlations")
    fig.tight_layout()
    fig.savefig(charts_dir / "correlation.png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    return [
        "## Criterion mark correlations",
        "",
        "![Criterion mark correlations](assets/correlation.png)",
        "",
    ]


def _md_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    widths = [len(h) for h in headers]
    for row in rows:
        for col_idx, cell in enumerate(row):
            widths[col_idx] = max(widths[col_idx], len(cell))
    sep = "| " + " | ".join("-" * w for w in widths) + " |"

    def fmt(cells: list[str]) -> str:
        return "| " + " | ".join(c.ljust(widths[i]) for i, c in enumerate(cells)) + " |"

    return [fmt(headers), sep] + [fmt(row) for row in rows]


def _generate_band_table(all_totals: list[int], bands: list[Band]) -> list[str]:
    sorted_bands = sorted(bands, key=lambda b: b.min)
    count = len(all_totals)
    rows: list[list[str]] = []
    for idx, band in enumerate(sorted_bands):
        lower = band.min
        upper = sorted_bands[idx + 1].min if idx + 1 < len(sorted_bands) else None
        if upper is None:
            range_str = f"≥ {lower}"
            band_count = sum(1 for t in all_totals if t >= lower)
        else:
            range_str = f"{lower}–{upper - 1}"
            band_count = sum(1 for t in all_totals if lower <= t < upper)
        pct = 100 * band_count / count
        rows.append([band.name, range_str, str(band_count), f"{pct:.1f}%"])
    return (
        ["## Grade bands", ""]
        + _md_table(["Band", "Range", "Students", "%"], rows)
        + [""]
    )


def _generate_charts(
    all_totals: list[int],
    per_criterion_mark_values: dict[str, list[int]],
    criterion_names: list[str],
    complete_mark_rows: list[list[int]],
    charts_dir: Path,
    bands: list[Band] | None = None,
) -> list[str]:
    charts_dir.mkdir(parents=True, exist_ok=True)
    lines = _generate_distribution_chart(all_totals, charts_dir, bands)
    if len(all_totals) >= 2:
        lines += _generate_cumulative_chart(all_totals, charts_dir, bands)
        lines += _generate_boxplot_chart(per_criterion_mark_values, charts_dir)
        if len(criterion_names) >= 2:
            lines += _generate_correlation_chart(
                criterion_names, complete_mark_rows, charts_dir
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
    cumulative distribution, per-criterion boxplot, and (with at least two
    criteria and two complete students) a correlation heatmap.
    """
    bands = scheme.bands
    scheme_criterion_names = scheme.criterion_names()
    all_totals: list[int] = []
    per_criterion_categories: dict[str, dict[str, int]] = {
        q: {} for q in scheme_criterion_names
    }
    per_criterion_mark_values: dict[str, list[int]] = {
        q: [] for q in scheme_criterion_names
    }
    complete_mark_rows: list[list[int]] = []

    for student in students.students:
        total = compute_total_marks(student, scheme)
        criterion_marks = compute_criterion_marks(student, scheme)

        if total is not None:
            all_totals.append(total)
            complete_mark_rows.append(
                [
                    m
                    for q in scheme_criterion_names
                    if (m := criterion_marks[q]) is not None
                ]
            )

        for criterion_name in scheme_criterion_names:
            category_id = student.assignments.get(criterion_name, "")
            if category_id:
                counter = per_criterion_categories[criterion_name]
                counter[category_id] = counter.get(category_id, 0) + 1
            marks = criterion_marks.get(criterion_name)
            if marks is not None:
                per_criterion_mark_values[criterion_name].append(marks)

    lines: list[str] = ["# Marking summary", ""]

    if all_totals:
        count = len(all_totals)
        mean = statistics.mean(all_totals)
        std = statistics.stdev(all_totals) if count > 1 else 0.0
        minimum = min(all_totals)
        maximum = max(all_totals)
        if count >= 2:
            q1, median, q3 = statistics.quantiles(all_totals, n=4)
        else:
            q1 = median = q3 = float(all_totals[0])
        stat_rows = [
            ["Count", str(count)],
            ["Mean", f"{mean:.2f}"],
            ["Std dev", f"{std:.2f}"],
            ["Min", str(minimum)],
            ["Q1 (25%)", f"{q1:.2f}"],
            ["Median", f"{median:.2f}"],
            ["Q3 (75%)", f"{q3:.2f}"],
            ["Max", str(maximum)],
        ]
        lines += _md_table(["Statistic", "Value"], stat_rows) + [""]
        if bands:
            lines += _generate_band_table(all_totals, bands)
        if charts_dir is not None:
            lines += _generate_charts(
                all_totals,
                per_criterion_mark_values,
                scheme_criterion_names,
                complete_mark_rows,
                charts_dir,
                bands if bands else None,
            )
    else:
        lines += ["No complete marks yet.", ""]

    lines += ["## Per-criterion breakdown", ""]

    for criterion_name, category_counts in per_criterion_categories.items():
        criterion = scheme.criteria[criterion_name]
        lines += [f"### {criterion_name}", ""]
        for category_id, category in criterion.categories.items():
            count = category_counts.get(category_id, 0)
            label = category.feedback.removesuffix(".")
            lines.append(f"- {label}: {count} student(s) ({category.marks} marks)")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


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
