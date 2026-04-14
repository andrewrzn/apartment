import streamlit as st
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Callable

st.set_page_config(
    page_title="Геометрия квартиры: 5 класс",
    page_icon="📐",
    layout="wide"
)

# ---------- МОДЕЛЬ ЗАДАЧ ----------

@dataclass
class Problem:
    id: str
    lvl: str                # "Базовый", "Средний", "Продвинутый"
    title: str
    text: str
    steps: List[str]
    answer_text: str        # строка для показа
    answer_value: float     # числовой ответ (0.0, если не проверяем числом)
    answer_label: str       # подпись к полю ввода
    draw: Callable[[plt.Axes], None]


# ---------- СЕССИОННОЕ СОСТОЯНИЕ ----------

if "name" not in st.session_state:
    st.session_state["name"] = ""
if "grade" not in st.session_state:
    st.session_state["grade"] = ""
if "stats" not in st.session_state:
    st.session_state["stats"] = {
        "attempts": 0,
        "success": 0,
    }

# ---------- ТЕОРИЯ ----------

theory_cards = [
    ("🔲", "Квадрат", "Периметр квадрата: P = 4·a. Чтобы найти сторону: a = P / 4."),
    ("▭", "Прямоугольник", "Площадь: S = a·b (длина на ширину)."),
    ("🧩", "План квартиры", "Общая высота/ширина квартиры — это сумма высот/ширин всех комнат и коридора."),
]


# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ РИСОВАНИЯ ----------

def draw_rect(ax: plt.Axes, x, y, w, h, label="", fc="#ffffff", ec="#000000"):
    ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=2))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=7)


def draw_dim_h(ax: plt.Axes, x1, x2, y, text):
    ax.plot([x1, x2], [y, y], color="#dd6b20", linewidth=1)
    ax.text((x1 + x2) / 2, y - 0.15, text, ha="center", va="top", fontsize=7, color="#dd6b20")


def draw_dim_v(ax: plt.Axes, y1, y2, x, text):
    ax.plot([x, x], [y1, y2], color="#dd6b20", linewidth=1)
    ax.text(x - 0.15, (y1 + y2) / 2, text, ha="right", va="center", fontsize=7,
            color="#dd6b20", rotation="vertical")


# ---------- ОПРЕДЕЛЕНИЕ ЗАДАЧ ----------

problems: List[Problem] = []

# === БАЗОВЫЙ УРОВЕНЬ: Б1–Б5 ===

# Б1
def draw_B1(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 0, 0, 4, 4, "Комната", "#dcfce7")
    draw_rect(ax, 4, 0, 6, 4, "Коридор", "#e0f2fe")
    draw_dim_v(ax, 0, 4, -0.2, "4 м")
    draw_dim_h(ax, 4, 10, -0.3, "6 м")
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 4.7)
    ax.axis("off")

problems.append(Problem(
    id="B1",
    lvl="Базовый",
    title="Б1. Квадрат и коридор",
    text="Квадратная комната имеет периметр 16 м. К ней примыкает коридор: "
         "его ширина равна стороне комнаты, а длина на 2 м больше стороны комнаты. "
         "Найдите площадь коридора.",
    steps=[
        "Сторона комнаты: 16 : 4 = 4 м.",
        "Ширина коридора = 4 м, длина: 4 + 2 = 6 м.",
        "Площадь коридора: S = 4 · 6 = 24 м²."
    ],
    answer_text="24 м²",
    answer_value=24.0,
    answer_label="Площадь коридора, м²",
    draw=draw_B1
))

# Б2
def draw_B2(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 0, 0, 5, 5, "Комната", "#ffffff")
    draw_rect(ax, 0, 5, 5, 2, "Балкон", "#ffedd5")
    draw_dim_h(ax, 0, 5, -0.3, "5 м")
    draw_dim_v(ax, 5, 7, 5.2, "2 м")
    ax.set_xlim(-0.5, 6)
    ax.set_ylim(-0.5, 7.5)
    ax.axis("off")

problems.append(Problem(
    id="B2",
    lvl="Базовый",
    title="Б2. Балкон",
    text="Квадратная комната имеет периметр 20 м. По одной стороне комнаты сделан прямоугольный "
         "балкон шириной 2 м и такой же длины, как сторона комнаты. Найдите площадь балкона.",
    steps=[
        "Сторона комнаты: 20 : 4 = 5 м.",
        "Балкон: длина 5 м, ширина 2 м.",
        "Площадь балкона: S = 5 · 2 = 10 м²."
    ],
    answer_text="10 м²",
    answer_value=10.0,
    answer_label="Площадь балкона, м²",
    draw=draw_B2
))

# Б3
def draw_B3(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 2, 0, 3, 3, "К1", "#ffffff")
    draw_rect(ax, 0, 0, 2, 3, "Коридор", "#e0f2fe")
    draw_dim_h(ax, 0, 2, -0.3, "2 м")
    draw_dim_v(ax, 0, 3, 4.5, "3 м")
    ax.set_xlim(-0.5, 6)
    ax.set_ylim(-0.5, 4.5)
    ax.axis("off")

problems.append(Problem(
    id="B3",
    lvl="Базовый",
    title="Б3. Коридор слева",
    text="Комната 1 — квадрат с периметром 12 м. Слева от неё находится прямоугольный коридор "
         "длиной 2 м и такой же высоты, как комната. Найдите площадь коридора.",
    steps=[
        "Сторона комнаты: 12 : 4 = 3 м.",
        "Коридор: высота 3 м, длина 2 м.",
        "Площадь коридора: S = 3 · 2 = 6 м²."
    ],
    answer_text="6 м²",
    answer_value=6.0,
    answer_label="Площадь коридора, м²",
    draw=draw_B3
))

# Б4
def draw_B4(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 0, 0, 6, 6, "Комната", "#ffffff")
    draw_rect(ax, 6, 0, 3, 6, "Коридор", "#e0f2fe")
    draw_dim_h(ax, 0, 6, -0.3, "6 м")
    draw_dim_h(ax, 6, 9, -0.3, "3 м")
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 6.8)
    ax.axis("off")

problems.append(Problem(
    id="B4",
    lvl="Базовый",
    title="Б4. Коридор вдоль стороны",
    text="Квадратная комната имеет периметр 24 м. Вдоль одной её стороны проходит коридор шириной "
         "3 м и длиной, равной стороне комнаты. Найдите площадь коридора.",
    steps=[
        "Сторона комнаты: 24 : 4 = 6 м.",
        "Коридор: 6 м × 3 м.",
        "Площадь коридора: S = 6 · 3 = 18 м²."
    ],
    answer_text="18 м²",
    answer_value=18.0,
    answer_label="Площадь коридора, м²",
    draw=draw_B4
))

# Б5
def draw_B5(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 0, 0, 4, 4, "К1", "#dcfce7")
    draw_rect(ax, 0, 4, 4, 4, "К2", "#dcfce7")
    draw_rect(ax, 4, 0, 2, 8, "Коридор", "#e0f2fe")
    draw_dim_v(ax, 0, 8, -0.3, "8 м")
    draw_dim_h(ax, 4, 6, -0.3, "2 м")
    ax.set_xlim(-0.5, 6.8)
    ax.set_ylim(-0.5, 8.8)
    ax.axis("off")

problems.append(Problem(
    id="B5",
    lvl="Базовый",
    title="Б5. Две комнаты и коридор",
    text="Комната 1 и Комната 2 — квадраты 4×4 м. Справа — прямоугольный коридор высотой 8 м и "
         "шириной 2 м. Найдите площадь коридора.",
    steps=[
        "Общая высота слева: 4 + 4 = 8 м.",
        "Коридор: 8 м × 2 м.",
        "Площадь коридора: S = 8 · 2 = 16 м²."
    ],
    answer_text="16 м²",
    answer_value=16.0,
    answer_label="Площадь коридора, м²",
    draw=draw_B5
))

# === СРЕДНИЙ УРОВЕНЬ: С1–С5 ===

# С1
def draw_C1(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 0, 0, 4, 4, "К1(4)", "#ffffff")
    draw_rect(ax, 0, 4, 4, 6, "К2(6)", "#ffffff")
    draw_rect(ax, 4, 0, 10, 10, "К3(10)", "#ffffff")
    # выделяем коридор (нижняя часть К3 высотой 6)
    draw_rect(ax, 4, 0, 10, 6, "", "#e0f2fe")
    draw_dim_v(ax, 0, 10, -0.3, "10 м")
    draw_dim_h(ax, 4, 14, -0.3, "10 м")
    ax.set_xlim(-0.5, 14.8)
    ax.set_ylim(-0.5, 10.8)
    ax.axis("off")

problems.append(Problem(
    id="C1",
    lvl="Средний",
    title="С1. Три комнаты",
    text="Комната 1 — квадрат с периметром 16 м, снизу слева. Над ней комната 2 со стороной 6 м. "
         "Справа квадратная комната 3, высота всей квартиры 10 м. Под комнатой 3 — коридор. "
         "Найдите площадь коридора.",
    steps=[
        "Сторона К1: 16 : 4 = 4 м.",
        "Общая высота слева: 4 + 6 = 10 м ⇒ сторона К3 = 10 м.",
        "Коридор под К3: высота 10 − 4 = 6 м, ширина 10 м.",
        "Площадь коридора: S = 6 · 10 = 60 м²."
    ],
    answer_text="60 м²",
    answer_value=60.0,
    answer_label="Площадь коридора, м²",
    draw=draw_C1
))

# С2
def draw_C2(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 0, 0, 4, 4, "К1(4)", "#ffffff")
    draw_rect(ax, 0, 4, 4, 3, "К2(3)", "#ffffff")
    draw_rect(ax, 4, 0, 7, 7, "К4(7)", "#ffffff")
    draw_rect(ax, 4, 4, 3, 3, "К3(3)", "#ffffff")
    draw_rect(ax, 4, 0, 2, 4, "Кор", "#e0f2fe")
    draw_dim_h(ax, 4, 6, -0.3, "2 м")
    draw_dim_v(ax, 0, 4, 6.2, "4 м")
    ax.set_xlim(-0.5, 11.8)
    ax.set_ylim(-0.5, 7.8)
    ax.axis("off")

problems.append(Problem(
    id="C2",
    lvl="Средний",
    title="С2. Периметр и коридор",
    text="К1 (P=16) снизу слева, над ней К2. Справа квадрат К4 (P=28). Над коридором — комната 3. "
         "Все комнаты квадратные. Найдите площадь коридора.",
    steps=[
        "a1 = 4, a4 = 7. Высота квартиры = 7 м.",
        "a2 = 7 − 4 = 3 м, К3 тоже 3×3.",
        "Коридор 4 м высотой и 2 м шириной.",
        "Площадь коридора: S = 4 · 2 = 8 м²."
    ],
    answer_text="8 м²",
    answer_value=8.0,
    answer_label="Площадь коридора, м²",
    draw=draw_C2
))

# С3
def draw_C3(ax):
    ax.set_aspect("equal")
    # К1 5×5
    draw_rect(ax, 0, 0, 5, 5, "К1(5)", "#ffffff")
    # К2 7×7 над К1
    draw_rect(ax, 0, 5, 5, 7, "К2(7)", "#ffffff")
    # К3 12×12 справа
    draw_rect(ax, 5, 0, 12, 12, "К3(12)", "#ffffff")
    # Коридор под К3: высота 5, ширина 12
    draw_rect(ax, 5, 0, 12, 5, "Кор", "#e0f2fe")
    draw_dim_v(ax, 0, 12, -0.3, "12 м")
    draw_dim_h(ax, 5, 17, -0.3, "12 м")
    ax.set_xlim(-0.5, 17.5)
    ax.set_ylim(-0.5, 12.8)
    ax.axis("off")

problems.append(Problem(
    id="C3",
    lvl="Средний",
    title="С3. Высокая комната",
    text="Комната 1 — квадрат с периметром 20 м. Над ней квадратная комната 2 с периметром 28 м. "
         "Справа от комнаты 2 находится квадратная комната 3, так что общая высота слева и справа одинакова. "
         "Под комнатой 3 располагается коридор. Найдите площадь коридора.",
    steps=[
        "К1: P=20 → a1=5 м. К2: P=28 → a2=7 м.",
        "Высота слева: 5+7=12 м, значит сторона К3=12 м.",
        "Коридор под К3: высота 12−7=5 м, ширина 12 м.",
        "Площадь коридора: S = 5 · 12 = 60 м²."
    ],
    answer_text="60 м²",
    answer_value=60.0,
    answer_label="Площадь коридора, м²",
    draw=draw_C3
))

# С4
def draw_C4(ax):
    ax.set_aspect("equal")
    # К1 4×4
    draw_rect(ax, 0, 0, 4, 4, "К1(4)", "#ffffff")
    # К2 3×3 над К1
    draw_rect(ax, 0, 4, 4, 3, "К2(3)", "#ffffff")
    # К3 5×5 справа сверху
    draw_rect(ax, 4, 4, 5, 5, "К3(5)", "#ffffff")
    # Коридор под К3: высота 2 (7-5), ширина 5
    draw_rect(ax, 4, 0, 5, 2, "Кор", "#e0f2fe")
    draw_dim_v(ax, 0, 7, -0.3, "7 м")
    draw_dim_h(ax, 4, 9, -0.3, "5 м")
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-0.5, 7.8)
    ax.axis("off")

problems.append(Problem(
    id="C4",
    lvl="Средний",
    title="С4. Малый коридор",
    text="Комната 1 — квадрат 4×4 м. Над ней квадратная комната 2 3×3 м. Справа от комнаты 2 — "
         "квадратная комната 3 5×5 м. Под комнатой 3 — прямоугольный коридор. Общая высота квартиры "
         "равна сумме высот комнаты 1 и комнаты 2. Найдите площадь коридора.",
    steps=[
        "Высота слева: 4 + 3 = 7 м.",
        "Комната 3 высотой 5 м, значит под ней остаётся 7−5=2 м.",
        "Коридор: 2×5.",
        "Площадь коридора: S = 2 · 5 = 10 м²."
    ],
    answer_text="10 м²",
    answer_value=10.0,
    answer_label="Площадь коридора, м²",
    draw=draw_C4
))

# С5
def draw_C5(ax):
    ax.set_aspect("equal")
    # К1 6×6
    draw_rect(ax, 0, 0, 6, 6, "К1(6)", "#ffffff")
    # К2 4×4 над К1
    draw_rect(ax, 0, 6, 6, 4, "К2(4)", "#ffffff")
    # К3 6×4 (комната 3)
    draw_rect(ax, 6, 6, 6, 4, "К3(6×4)", "#ffffff")
    # Коридор под К3: 6×6
    draw_rect(ax, 6, 0, 6, 6, "Кор", "#e0f2fe")
    draw_dim_v(ax, 0, 10, -0.3, "10 м")
    draw_dim_h(ax, 6, 12, -0.3, "6 м")
    ax.set_xlim(-0.5, 12.8)
    ax.set_ylim(-0.5, 10.8)
    ax.axis("off")

problems.append(Problem(
    id="C5",
    lvl="Средний",
    title="С5. Коридор и комната 3",
    text="Комната 1 — квадрат со стороной 6 м. Над ней квадратная комната 2 со стороной 4 м. "
         "Справа от комнаты 2 и комнаты 1 расположены два прямоугольника одинаковой ширины: "
         "верхний — комната 3 (6×4 м), нижний — коридор. Высота всей квартиры 10 м. "
         "Найдите площадь коридора.",
    steps=[
        "Высота слева: 6 + 4 = 10 м — совпадает с общей.",
        "Комната 3: 6×4, значит под ней коридор высотой 6 (10−4).",
        "Ширина коридора = 6 м.",
        "Площадь коридора: S = 6 · 6 = 36 м²."
    ],
    answer_text="36 м²",
    answer_value=36.0,
    answer_label="Площадь коридора, м²",
    draw=draw_C5
))

# === ПРОДВИНУТЫЙ УРОВЕНЬ: П1–П5 ===

# П1
def draw_P1(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 0, 0, 3, 3, "a1", "#ffffff")
    draw_rect(ax, 0, 3, 3, 4, "a2", "#ffffff")
    draw_rect(ax, 3, 0, 5, 7, "a3", "#ffffff")
    draw_rect(ax, 3, 0, 5, 1, "Кор", "#fee2e2")
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-0.5, 7.8)
    ax.axis("off")

problems.append(Problem(
    id="P1",
    lvl="Продвинутый",
    title="П1. Выражение через P1",
    text="Комната 1 — квадрат, её периметр P1. Над ней комната 2, периметр которой на 8 м больше. "
         "Справа квадратная комната 3, её периметр на 16 м больше, чем у комнаты 2. "
         "Под комнатой 3 — коридор. Выразите площадь коридора через P1.",
    steps=[
        "Пусть сторона комнаты 1: a1 = P1 / 4.",
        "Тогда a2 = a1 + 2, a3 = a2 + 4 = a1 + 6.",
        "Высота слева: a1 + a2 = 2a1 + 2.",
        "Высота коридора: (2a1 + 2) − (a1 + 6) = a1 − 4.",
        "Ширина коридора: a3 = a1 + 6.",
        "Площадь коридора: S = (a1 − 4)(a1 + 6)."
    ],
    answer_text="S = (a1 − 4)(a1 + 6)",
    answer_value=0.0,
    answer_label="(для этой задачи проверь себя по решению ниже)",
    draw=draw_P1
))

# П2 (обратная задача)
def draw_P2(ax):
    ax.set_aspect("equal")
    # К1 3×3
    draw_rect(ax, 0, 0, 3, 3, "К1(3)", "#ffffff")
    # Коридор 7×3
    draw_rect(ax, 3, 0, 7, 3, "Кор", "#e0f2fe")
    # К2 и К3 5×5 сверху
    draw_rect(ax, 0, 3, 5, 5, "К2(5)", "#ffffff")
    draw_rect(ax, 5, 3, 5, 5, "К3(5)", "#ffffff")
    # К4 8×8 справа
    draw_rect(ax, 10, 0, 8, 8, "К4(8)", "#ffffff")
    ax.set_xlim(-0.5, 18.5)
    ax.set_ylim(-0.5, 8.8)
    ax.axis("off")

problems.append(Problem(
    id="P2",
    lvl="Продвинутый",
    title="П2. Восстановление плана",
    text="Высота коридора 3 м, его площадь 21 м². Комната 1 — квадрат 3×3, находится внизу слева. "
         "По этим данным восстановите периметры остальных квадратных комнат, если план как в примере.",
    steps=[
        "Высота коридора: 3 м, площадь 21 м² → длина 7 м.",
        "Снизу: 3 + 7 = 10 м — это ширина верхнего ряда (К2 и К3).",
        "Комнаты К2 и К3 имеют сторону 5 м (10 = 5+5).",
        "Правая большая комната К4: сторона 8 м (из исходного примера).",
        "Периметры: К1 — 12 м, К2 — 20 м, К3 — 20 м, К4 — 32 м."
    ],
    answer_text="Периметры: 12, 20, 20, 32 м.",
    answer_value=0.0,
    answer_label="(здесь ответ — набор периметров, смотри решение)",
    draw=draw_P2
))

# П3
def draw_P3(ax):
    ax.set_aspect("equal")
    # К1 4×4
    draw_rect(ax, 0, 0, 4, 4, "К1(4)", "#ffffff")
    # К2 6×6 над К1
    draw_rect(ax, 0, 4, 4, 6, "К2(6)", "#ffffff")
    # К3 6×6 справа сверху
    draw_rect(ax, 4, 4, 6, 6, "К3(6)", "#ffffff")
    # К4 10×10 справа
    draw_rect(ax, 10, 0, 10, 10, "К4(10)", "#ffffff")
    # Коридор 6×4 под К3
    draw_rect(ax, 4, 0, 6, 4, "Кор", "#e0f2fe")
    ax.set_xlim(-0.5, 21)
    ax.set_ylim(-0.5, 10.8)
    ax.axis("off")

problems.append(Problem(
    id="P3",
    lvl="Продвинутый",
    title="П3. Стороны комнат 2 и 3",
    text="Комната 4 — квадрат, её периметр 40 м. Слева снизу — квадратная комната 1 с периметром 16 м, "
         "над ней квадратная комната 2, над коридором — квадратная комната 3. План аналогичен схеме примера. "
         "Найдите стороны комнат 2 и 3 и площадь коридора.",
    steps=[
        "К1: P=16 → a1=4 м. К4: P=40 → a4=10 м.",
        "Высота квартиры 10 м. Тогда a2 = 10 − 4 = 6 м.",
        "Комната 3 — квадрат, возьмём сторону a3 = 6 м.",
        "Коридор под К3: высота 4 м, ширина 6 м.",
        "Площадь коридора: S = 4 · 6 = 24 м²."
    ],
    answer_text="a2=6 м, a3=6 м, S=24 м²",
    answer_value=24.0,
    answer_label="Площадь коридора, м²",
    draw=draw_P3
))

# П4
def draw_P4(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 0, 0, 3, 3, "a", "#ffffff")
    draw_rect(ax, 0, 3, 3, 4, "a+1", "#ffffff")
    draw_rect(ax, 3, 0, 5, 7, "a+3", "#ffffff")
    draw_rect(ax, 3, 0, 5, 2, "Кор", "#fee2e2")
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-0.5, 7.8)
    ax.axis("off")

problems.append(Problem(
    id="P4",
    lvl="Продвинутый",
    title="П4. Переменная a",
    text="Комната 1 — квадрат, её сторона a метров. Над ней квадратная комната 2 со стороной a+1 м. "
         "Справа от комнаты 2 — квадратная комната 3 со стороной a+3 м, под ней — коридор. "
         "Общая высота квартиры равна 2a+1 м. Найдите площадь коридора через a.",
    steps=[
        "Высота слева: a + (a+1) = 2a+1 — совпадает с общей высотой.",
        "Справа: комната 3 высотой a+3.",
        "Высота коридора: (2a+1) − (a+3) = a−2.",
        "Ширина коридора: a+3.",
        "Площадь: S = (a−2)(a+3)."
    ],
    answer_text="S = (a−2)(a+3)",
    answer_value=0.0,
    answer_label="(ответ — выражение, смотри решение)",
    draw=draw_P4
))

# П5
def draw_P5(ax):
    ax.set_aspect("equal")
    # К1 3×3
    draw_rect(ax, 0, 0, 3, 3, "К1(3)", "#ffffff")
    # К2 4×4 над К1
    draw_rect(ax, 0, 3, 4, 4, "К2(4)", "#ffffff")
    # К3 8×8 справа
    draw_rect(ax, 4, 0, 8, 8, "К3(8)", "#ffffff")
    # Коридор 8×3 под К3
    draw_rect(ax, 4, 0, 8, 3, "Кор", "#e0f2fe")
    ax.set_xlim(-0.5, 13)
    ax.set_ylim(-0.5, 8.8)
    ax.axis("off")

problems.append(Problem(
    id="P5",
    lvl="Продвинутый",
    title="П5. Три квадрата и коридор",
    text="В квартире три квадратные комнаты и коридор. "
         "Нижняя левая комната имеет периметр 12 м, верхняя левая — периметр 16 м, правая — периметр 32 м. "
         "Коридор занимает нижнее правое место и его высота равна высоте нижней левой комнаты. "
         "Найдите площадь коридора.",
    steps=[
        "Нижняя левая: P=12 → сторона 3 м.",
        "Верхняя левая: P=16 → сторона 4 м.",
        "Правая комната: P=32 → сторона 8 м.",
        "Высота коридора = высоте нижней комнаты = 3 м, ширина = 8 м.",
        "Площадь коридора: S = 3 · 8 = 24 м²."
    ],
    answer_text="24 м²",
    answer_value=24.0,
    answer_label="Площадь коридора, м²",
    draw=draw_P5
))


# ---------- UI ----------

st.title("📐 Геометрия квартиры: 5 класс")
st.markdown("Интерактивные задачи на план квартиры и площадь коридора.")

tab_theory, tab_practice = st.tabs(["Правила", "Задачи"])

with tab_theory:
    st.subheader("Наши инструменты")
    cols = st.columns(len(theory_cards))
    for col, (icon, title, desc) in zip(cols, theory_cards):
        with col:
            st.markdown(f"### {icon} {title}")
            st.write(desc)

with tab_practice:
    # Личный кабинет
    st.subheader("Личный кабинет")

    col_name, col_grade = st.columns(2)
    with col_name:
        name = st.text_input("Имя ученика", value=st.session_state["name"])
    with col_grade:
        grade = st.text_input("Класс", value=st.session_state["grade"])

    st.session_state["name"] = name
    st.session_state["grade"] = grade

    if name:
        st.markdown(f"**Привет, {name}!**")
    if grade:
        st.markdown(f"Класс: {grade}")

    st.markdown("---")

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.subheader("Сложность")
        levels = ["Базовый", "Средний", "Продвинутый"]
        current_level = st.radio("Выберите уровень", levels)

        st.subheader("Выбор задачи")
        filtered = [p for p in problems if p.lvl == current_level]
        if not filtered:
            st.info("Для этого уровня задачи пока нет.")
            selected_title = None
        else:
            titles = [p.title for p in filtered]
            selected_title = st.selectbox("Задача", titles)

    with col_right:
        if not filtered or selected_title is None:
            st.info("Выберите задачу слева.")
        else:
            problem = next(p for p in filtered if p.title == selected_title)

            st.markdown(f"### {problem.title}")
            st.markdown(f"**Уровень:** {problem.lvl}")
            st.markdown("#### Чертёж")

            fig, ax = plt.subplots(figsize=(2.8, 2.2))
            problem.draw(ax)
            st.pyplot(fig)

            st.markdown("#### Условие")
            st.write(problem.text)

            can_check_numeric = problem.answer_value != 0.0

            if can_check_numeric:
                st.markdown("#### Попробуй решить сам")
                user_value = st.number_input(
                    problem.answer_label,
                    value=0.0,
                    step=1.0,
                    format="%.1f",
                    key=f"answer_{problem.id}"
                )
                check = st.button("Проверить ответ", key=f"check_{problem.id}")
                if check:
                    st.session_state["stats"]["attempts"] += 1
                    if abs(user_value - problem.answer_value) < 1e-6:
                        st.session_state["stats"]["success"] += 1
                        st.success("Отлично! Ответ верный 🎉")
                        st.balloons()
                    else:
                        st.error("Пока неверно. Посмотри решение ниже и попробуй ещё раз.")
            else:
                st.info("Для этой задачи ответ не число. Проверь себя по решению ниже.")

            show_solution = st.toggle("Показать решение", value=False, key=f"sol_{problem.id}")
            if show_solution:
                st.markdown("#### Пошаговое решение")
                for i, step in enumerate(problem.steps, start=1):
                    st.markdown(f"**{i}.** {step}")
                st.markdown(f"**Ответ:** {problem.answer_text}")

    st.markdown("---")
    st.subheader("Твоя статистика за этот сеанс")
    stats = st.session_state["stats"]
    st.write(f"Всего попыток: {stats['attempts']}")
    st.write(f"Удачных попыток: {stats['success']}")
    if stats["attempts"] > 0:
        rate = stats["success"] / stats["attempts"] * 100
        st.write(f"Процент верных ответов: {rate:.1f}%")
