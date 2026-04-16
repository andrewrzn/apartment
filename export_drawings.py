#!/usr/bin/env python3
"""Сохранить чертежи всех задач в PNG (то же, что делает export_workbook с чертежами)."""
from __future__ import annotations

import argparse
from pathlib import Path

from export_workbook import render_problem_figures
from problems_catalog import problems


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("workbook_figures"),
        help="Папка для PNG (по умолчанию workbook_figures)",
    )
    args = ap.parse_args()
    render_problem_figures(args.output_dir)
    print(f"Written {len(problems)} files to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
