#!/usr/bin/env python3
"""
Сборка методички-задачника из каталога задач (без Streamlit).

Чертежи: по умолчанию перерисовываются в PNG и вставляются в Markdown рядом с текстом
(пути относительные — картинки подхватываются при просмотре .md и при конвертации в DOCX/PDF).

Ответы: в полной версии у каждой задачи блок «Ответ: …», опция --student-only убирает и решение, и ответ.
Сводная таблица ответов: --answers-table (только вместе с полной версией).

Примеры:
  python export_workbook.py
  python export_workbook.py -o out/методичка.md --figures-dir out/img
  python export_workbook.py --student-only -o задачи_без_ответов.md
  python export_workbook.py --no-figures
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from problems_catalog import problems


def render_problem_figures(figures_dir: Path) -> None:
    figures_dir.mkdir(parents=True, exist_ok=True)
    for p in problems:
        fig, ax = plt.subplots(figsize=(4.8, 3.6), dpi=130)
        p.draw(ax)
        fig.patch.set_facecolor("white")
        out = figures_dir / f"{p.id}.png"
        fig.savefig(
            out,
            format="png",
            bbox_inches="tight",
            pad_inches=0.05,
            facecolor="white",
            edgecolor="none",
        )
        plt.close(fig)


def _md_image_line(md_path: Path, png_path: Path) -> str:
    rel = os.path.relpath(png_path.resolve(), start=md_path.parent.resolve())
    return f"![Чертёж {png_path.stem}]({Path(rel).as_posix()})"


def main() -> None:
    ap = argparse.ArgumentParser(description="Экспорт задач, решений и ответов в Markdown")
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("methodology_workbook.md"),
        help="Файл вывода (по умолчанию methodology_workbook.md)",
    )
    ap.add_argument(
        "--figures-dir",
        type=Path,
        default=Path("workbook_figures"),
        help="Папка для PNG (по умолчанию workbook_figures)",
    )
    ap.add_argument(
        "--no-figures",
        action="store_true",
        help="Не генерировать PNG и не вставлять картинки (только текст)",
    )
    ap.add_argument(
        "--student-only",
        action="store_true",
        help="Только условия (без пошагового решения и без ответов; чертежи вставляются, если не указан --no-figures)",
    )
    ap.add_argument(
        "--answers-table",
        action="store_true",
        help="В конце добавить таблицу «задача — ответ»",
    )
    args = ap.parse_args()

    md_path = args.output
    figures_dir = args.figures_dir
    with_figures = not args.no_figures

    if with_figures:
        render_problem_figures(figures_dir)

    order = ["Базовый", "Средний", "Продвинутый"]
    by_lvl: dict[str, list] = {lv: [] for lv in order}
    for p in problems:
        if p.lvl in by_lvl:
            by_lvl[p.lvl].append(p)

    lines: list[str] = [
        "# Геометрия квартиры — задачник (5 класс)",
        "",
        "Текст и чертежи сформированы из того же каталога, что и интерактивное приложение.",
        "",
    ]

    for lv in order:
        ps = by_lvl[lv]
        if not ps:
            continue
        lines.append(f"## {lv}")
        lines.append("")
        for p in ps:
            lines.append(f"### {p.title}")
            lines.append("")
            if with_figures:
                png = (figures_dir / f"{p.id}.png").resolve()
                lines.append(_md_image_line(md_path, png))
                lines.append("")
            lines.append(f"**Условие.** {p.text}")
            lines.append("")
            if not args.student_only:
                lines.append("**Решение.**")
                for i, step in enumerate(p.steps, start=1):
                    lines.append(f"{i}. {step}")
                lines.append("")
                lines.append(f"**Ответ:** {p.answer_text}")
                lines.append("")
            lines.append("---")
            lines.append("")

    if args.answers_table and not args.student_only:
        lines.append("## Сводная таблица ответов")
        lines.append("")
        lines.append("| Задача | Ответ |")
        lines.append("| --- | --- |")
        for p in problems:
            lines.append(f"| {p.id} | {p.answer_text} |")
        lines.append("")

    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines), encoding="utf-8")
    msg = f"Written: {md_path.resolve()} ({len(problems)} problems)"
    if with_figures:
        msg += f", figures: {figures_dir.resolve()}"
    print(msg)


if __name__ == "__main__":
    main()
