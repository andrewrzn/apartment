#!/usr/bin/env python3
"""
Экспорт методички для "Тренажер пропорций и площадей":
- задачи
- решения (объяснения)
- чертежи
- автосборка DOCX (если установлен pandoc)
"""
from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from proporsii_trenajer_module import TASKS


def render_proporsii_figures(figures_dir: Path) -> None:
    figures_dir.mkdir(parents=True, exist_ok=True)
    for t in TASKS:
        fig, ax = plt.subplots(figsize=(5.4, 2.8), dpi=140)
        t.draw(ax)
        fig.patch.set_facecolor("white")
        out = figures_dir / f"P{t.number}.png"
        fig.savefig(
            out,
            format="png",
            bbox_inches="tight",
            pad_inches=0.03,
            facecolor="white",
            edgecolor="none",
        )
        plt.close(fig)


def _md_image_line(md_path: Path, png_path: Path) -> str:
    rel = os.path.relpath(png_path.resolve(), start=md_path.parent.resolve())
    return f"![Чертёж задачи {png_path.stem}]({Path(rel).as_posix()})"


def _build_markdown(md_path: Path, figures_dir: Path, student_only: bool, answers_table: bool, with_figures: bool) -> None:
    order = ["Уровень 1", "Уровень 2", "Уровень 3"]
    by_lvl: dict[str, list] = {lv: [] for lv in order}
    for t in TASKS:
        by_lvl[t.level].append(t)

    lines: list[str] = [
        "# Тренажер пропорций и площадей — задачник (5 класс)",
        "",
        "Материал сформирован автоматически из интерактивного тренажера.",
        "",
    ]

    for lv in order:
        lines.append(f"## {lv}")
        lines.append("")
        for t in by_lvl[lv]:
            lines.append(f"### Задача {t.number}. {t.title}")
            lines.append("")
            if with_figures:
                png = (figures_dir / f"P{t.number}.png").resolve()
                lines.append(_md_image_line(md_path, png))
                lines.append("")
            lines.append(f"**Условие.** {t.text}")
            lines.append("")
            if not student_only:
                lines.append(f"**Решение.** {t.explanation}")
                lines.append("")
                lines.append(f"**Ответ:** {t.answer_text}")
                lines.append("")
            lines.append("---")
            lines.append("")

    if answers_table and not student_only:
        lines.append("## Сводная таблица ответов")
        lines.append("")
        lines.append("| Задача | Ответ |")
        lines.append("| --- | --- |")
        for t in TASKS:
            lines.append(f"| {t.number} | {t.answer_text} |")
        lines.append("")

    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines), encoding="utf-8")


def _export_docx(md_path: Path, docx_path: Path) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["pandoc", str(md_path), "-o", str(docx_path), "--resource-path=."],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return False, "pandoc not found"

    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown pandoc error"
        return False, stderr

    return True, ""


def main() -> None:
    ap = argparse.ArgumentParser(description="Экспорт задачника по пропорциям в Markdown и DOCX")
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("proporsii_workbook.md"),
        help="Markdown-файл вывода (по умолчанию proporsii_workbook.md)",
    )
    ap.add_argument(
        "--docx",
        type=Path,
        default=Path("proporsii_methodichka.docx"),
        help="DOCX-файл вывода (по умолчанию proporsii_methodichka.docx)",
    )
    ap.add_argument(
        "--figures-dir",
        type=Path,
        default=Path("proporsii_figures"),
        help="Папка для PNG чертежей (по умолчанию proporsii_figures)",
    )
    ap.add_argument("--no-figures", action="store_true", help="Не генерировать/не вставлять чертежи")
    ap.add_argument("--no-docx", action="store_true", help="Не собирать DOCX")
    ap.add_argument("--student-only", action="store_true", help="Только условия (без решений и ответов)")
    ap.add_argument("--answers-table", action="store_true", help="Добавить таблицу ответов в конец")
    args = ap.parse_args()

    with_figures = not args.no_figures
    if with_figures:
        render_proporsii_figures(args.figures_dir)

    _build_markdown(args.output, args.figures_dir, args.student_only, args.answers_table, with_figures)
    print(f"Written: {args.output.resolve()} ({len(TASKS)} tasks)")
    if with_figures:
        print(f"Figures: {args.figures_dir.resolve()}")

    if not args.no_docx:
        ok, err = _export_docx(args.output, args.docx)
        if ok:
            print(f"Written: {args.docx.resolve()}")
        else:
            print(f"DOCX skipped: {err}")


if __name__ == "__main__":
    main()

