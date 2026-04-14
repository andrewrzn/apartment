"""Чертежи планов квартир: общая сетка, ровные стыки, размерные линии."""
from __future__ import annotations

from matplotlib.patches import Rectangle

# Единица координат ≈ 1 м (поля зарезервированы под подписи)
DEFAULT_XMAX = 20.0
DEFAULT_YMAX = 16.0

ROOM = "#f8fafc"
ROOM_GREEN = "#dcfce7"
ROOM_BALC = "#ffedd5"
CORRIDOR = "#dbeafe"
CORRIDOR_ROSE = "#fee2e2"
EDGE = "#1e293b"
DIM_COLOR = "#c2410c"


def setup_axes(ax, xmax: float = DEFAULT_XMAX, ymax: float = DEFAULT_YMAX) -> None:
    ax.set_aspect("equal")
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.axis("off")
    ax.set_facecolor("#ffffff")


def setup_axes_tight(
    ax,
    xmax: float,
    ymax: float,
    *,
    xmin: float = 0.0,
    ymin: float = 0.0,
    pad: float = 0.2,
) -> None:
    """Оси по фактическому размеру плана — чертеж крупно заполняет картинку (для базовых задач)."""
    ax.set_aspect("equal")
    ax.set_xlim(xmin - pad, xmax + pad)
    ax.set_ylim(ymin - pad, ymax + pad)
    ax.axis("off")
    ax.set_facecolor("#ffffff")


def draw_rect(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str = "",
    *,
    fc: str = ROOM,
    ec: str = EDGE,
    lw: float = 1.65,
    zorder: int = 2,
    fontsize: int = 8,
) -> None:
    ax.add_patch(
        Rectangle(
            (x, y),
            w,
            h,
            facecolor=fc,
            edgecolor=ec,
            linewidth=lw,
            zorder=zorder,
            joinstyle="miter",
        )
    )
    if label:
        ax.text(
            x + w / 2,
            y + h / 2,
            label,
            ha="center",
            va="center",
            fontsize=fontsize,
            zorder=zorder + 1,
            color="#0f172a",
        )


def draw_dim_h(
    ax,
    x1: float,
    x2: float,
    y: float,
    text: str,
    *,
    color: str = DIM_COLOR,
    fontsize: int = 7,
) -> None:
    ax.plot([x1, x2], [y, y], color=color, linewidth=1.0, zorder=10)
    tick = 0.12
    ax.plot([x1, x1], [y - tick, y + tick], color=color, lw=1, zorder=10)
    ax.plot([x2, x2], [y - tick, y + tick], color=color, lw=1, zorder=10)
    ax.text(
        (x1 + x2) / 2,
        y - 0.32,
        text,
        ha="center",
        va="top",
        fontsize=fontsize,
        color=color,
        zorder=11,
    )


def draw_dim_v(
    ax,
    y1: float,
    y2: float,
    x: float,
    text: str,
    *,
    color: str = DIM_COLOR,
    fontsize: int = 7,
) -> None:
    ax.plot([x, x], [y1, y2], color=color, linewidth=1.0, zorder=10)
    tick = 0.12
    ax.plot([x - tick, x + tick], [y1, y1], color=color, lw=1, zorder=10)
    ax.plot([x - tick, x + tick], [y2, y2], color=color, lw=1, zorder=10)
    ax.text(
        x - 0.32,
        (y1 + y2) / 2,
        text,
        ha="right",
        va="center",
        fontsize=fontsize,
        color=color,
        rotation=90,
        zorder=11,
    )
