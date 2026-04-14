import io
import streamlit as st
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Callable

from drawing import (
    setup_axes,
    draw_rect,
    draw_dim_h,
    draw_dim_v,
    ROOM_GREEN,
    ROOM_BALC,
    CORRIDOR,
    CORRIDOR_ROSE,
)

st.set_page_config(
    page_title="Геометрия квартиры: 5 класс",
    page_icon="📐",
    layout="wide",
)

# На Streamlit Cloud колонки часто выравниваются по высоте — контент «уезжает» вниз;
# блок st.image иногда получает лишний min-height. CSS и vertical_alignment это исправляют.
st.markdown(
    """
    <style>
    div[data-testid="stImage"],
    div[data-testid="stImage"] > div {
        min-height: 0 !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        align-self: flex-start !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- МОДЕЛЬ ЗАДАЧ ----------


@dataclass
class Problem:
    id: str
    lvl: str  # "Базовый", "Средний", "Продвинутый"
    title: str
    text: str
    steps: List[str]
    answer_text: str
    answer_value: float
    answer_label: str
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

# ---------- ОПРЕДЕЛЕНИЕ ЗАДАЧ ----------

problems: List[Problem] = []

# === БАЗОВЫЙ УРОВЕНЬ: Б1–Б5 ===


def draw_B1(ax):
    setup_axes(ax)
    draw_rect(ax, 1, 1, 4, 4, "К", fc=ROOM_GREEN, zorder=3)
    draw_rect(ax, 5, 1, 6, 4, "Кор", fc=CORRIDOR, zorder=2)
    draw_dim_v(ax, 1, 5, 0.6, "4 м")
    draw_dim_h(ax, 5, 11, 0.4, "6 м")


problems.append(
    Problem(
        id="B1",
        lvl="Базовый",
        title="Б1. Квадрат и коридор",
        text="Квадратная комната имеет периметр 16 м. К ней примыкает коридор: "
        "его ширина равна стороне комнаты, а длина на 2 м больше стороны комнаты. "
        "Найдите площадь коридора.",
        steps=[
            "Сторона комнаты: 16 : 4 = 4 м.",
            "Ширина коридора = 4 м, длина: 4 + 2 = 6 м.",
            "Площадь коридора: S = 4 · 6 = 24 м².",
        ],
        answer_text="24 м²",
        answer_value=24.0,
        answer_label="Площадь коридора, м²",
        draw=draw_B1,
    )
)


def draw_B2(ax):
    setup_axes(ax)
    draw_rect(ax, 2, 1, 5, 5, "К", zorder=3)
    draw_rect(ax, 2, 6, 5, 2, "Балк", fc=ROOM_BALC, zorder=3)
    draw_dim_h(ax, 2, 7, 0.4, "5 м")
    draw_dim_v(ax, 6, 8, 7.1, "2 м")


problems.append(
    Problem(
        id="B2",
        lvl="Базовый",
        title="Б2. Балкон",
        text="Квадратная комната имеет периметр 20 м. По одной стороне комнаты сделан прямоугольный "
        "балкон шириной 2 м и такой же длины, как сторона комнаты. Найдите площадь балкона.",
        steps=[
            "Сторона комнаты: 20 : 4 = 5 м.",
            "Балкон: длина 5 м, ширина 2 м.",
            "Площадь балкона: S = 5 · 2 = 10 м².",
        ],
        answer_text="10 м²",
        answer_value=10.0,
        answer_label="Площадь балкона, м²",
        draw=draw_B2,
    )
)


def draw_B3(ax):
    setup_axes(ax)
    draw_rect(ax, 4, 1, 3, 3, "К1", zorder=3)
    draw_rect(ax, 2, 1, 2, 3, "Кор", fc=CORRIDOR, zorder=2)
    draw_dim_h(ax, 2, 4, 0.35, "2 м")
    draw_dim_v(ax, 1, 4, 7.1, "3 м")


problems.append(
    Problem(
        id="B3",
        lvl="Базовый",
        title="Б3. Коридор слева",
        text="Комната 1 — квадрат с периметром 12 м. Слева от неё находится прямоугольный коридор "
        "длиной 2 м и такой же высоты, как комната. Найдите площадь коридора.",
        steps=[
            "Сторона комнаты: 12 : 4 = 3 м.",
            "Коридор: высота 3 м, длина 2 м.",
            "Площадь коридора: S = 3 · 2 = 6 м².",
        ],
        answer_text="6 м²",
        answer_value=6.0,
        answer_label="Площадь коридора, м²",
        draw=draw_B3,
    )
)


def draw_B4(ax):
    setup_axes(ax)
    draw_rect(ax, 1, 1, 6, 6, "К", zorder=3)
    draw_rect(ax, 7, 1, 3, 6, "Кор", fc=CORRIDOR, zorder=2)
    draw_dim_h(ax, 1, 7, 0.4, "6 м")
    draw_dim_h(ax, 7, 10, 0.4, "3 м")


problems.append(
    Problem(
        id="B4",
        lvl="Базовый",
        title="Б4. Коридор вдоль стороны",
        text="Квадратная комната имеет периметр 24 м. Вдоль одной её стороны проходит коридор шириной "
        "3 м и длиной, равной стороне комнаты. Найдите площадь коридора.",
        steps=[
            "Сторона комнаты: 24 : 4 = 6 м.",
            "Коридор: 6 м × 3 м.",
            "Площадь коридора: S = 6 · 3 = 18 м².",
        ],
        answer_text="18 м²",
        answer_value=18.0,
        answer_label="Площадь коридора, м²",
        draw=draw_B4,
    )
)


def draw_B5(ax):
    setup_axes(ax)
    draw_rect(ax, 1, 1, 4, 4, "К1", fc=ROOM_GREEN, zorder=3)
    draw_rect(ax, 1, 5, 4, 4, "К2", fc=ROOM_GREEN, zorder=3)
    draw_rect(ax, 5, 1, 2, 8, "Кор", fc=CORRIDOR, zorder=2)
    draw_dim_v(ax, 2, 9, 0.55, "8 м")
    draw_dim_h(ax, 5, 7, 0.4, "2 м")


problems.append(
    Problem(
        id="B5",
        lvl="Базовый",
        title="Б5. Две комнаты и коридор",
        text="Комната 1 и Комната 2 — квадраты 4×4 м. Справа — прямоугольный коридор высотой 8 м и "
        "шириной 2 м. Найдите площадь коридора.",
        steps=[
            "Общая высота слева: 4 + 4 = 8 м.",
            "Коридор: 8 м × 2 м.",
            "Площадь коридора: S = 8 · 2 = 16 м².",
        ],
        answer_text="16 м²",
        answer_value=16.0,
        answer_label="Площадь коридора, м²",
        draw=draw_B5,
    )
)

# === СРЕДНИЙ УРОВЕНЬ ===


def draw_C1(ax):
    setup_axes(ax)
    # Слева: К1 4×4, К2 6×6 (квадрат); справа столбец 10 м: коридор 6×10, К3 4×10 (на плане прямоугольник)
    draw_rect(ax, 1, 1, 4, 4, "К1(4)", zorder=3)
    draw_rect(ax, 1, 5, 6, 6, "К2(6)", zorder=3)
    draw_rect(ax, 7, 1, 10, 6, "Кор", fc=CORRIDOR, zorder=2)
    draw_rect(ax, 7, 7, 10, 4, "К3", zorder=3)
    draw_dim_v(ax, 1, 11, 0.55, "10 м")
    draw_dim_h(ax, 7, 17, 0.45, "10 м")


problems.append(
    Problem(
        id="C1",
        lvl="Средний",
        title="С1. Три комнаты",
        text="Комната 1 — квадрат с периметром 16 м, снизу слева. Над ней квадратная комната 2 со стороной 6 м "
        "(левый столбец шириной 6 м, как на плане). Справа столбец шириной 10 м; высота всей квартиры 10 м. "
        "Сверху комната 3 размером 10×4 м, под ней — коридор. Найдите площадь коридора.",
        steps=[
            "Сторона К1: 16 : 4 = 4 м.",
            "Общая высота слева: 4 + 6 = 10 м.",
            "Комната 3 на плане имеет высоту 4 м, значит под ней коридор высотой 10 − 4 = 6 м; ширина столбца 10 м.",
            "Площадь коридора: S = 6 · 10 = 60 м².",
        ],
        answer_text="60 м²",
        answer_value=60.0,
        answer_label="Площадь коридора, м²",
        draw=draw_C1,
    )
)


def draw_C2(ax):
    setup_axes(ax)
    draw_rect(ax, 5, 1, 7, 7, "К4(7)", zorder=1)
    draw_rect(ax, 5, 1, 2, 4, "Кор", fc=CORRIDOR, zorder=4)
    draw_rect(ax, 1, 1, 4, 4, "К1(4)", zorder=3)
    draw_rect(ax, 1, 5, 3, 3, "К2(3)", zorder=3)
    draw_rect(ax, 5, 5, 3, 3, "К3(3)", zorder=3)
    draw_dim_h(ax, 5, 7, 0.45, "2 м")
    draw_dim_v(ax, 1, 5, 7.1, "4 м")


problems.append(
    Problem(
        id="C2",
        lvl="Средний",
        title="С2. Периметр и коридор",
        text="Комната 1 — квадрат с периметром 16 м, снизу слева. Над ней квадратная комната 2. "
        "Справа квадратная комната 4 с периметром 28 м. Над коридором расположена квадратная комната 3. "
        "Все комнаты квадратные. Найдите площадь коридора.",
        steps=[
            "К1: P=16 → a1=4 м. К4: P=28 → a4=7 м.",
            "Высота квартиры 7 м. Тогда сторона К2: a2 = 7 − 4 = 3 м.",
            "Комната 3 тоже 3×3, коридор под ней высотой 4 м и шириной 2 м.",
            "Площадь коридора: S = 4 · 2 = 8 м².",
        ],
        answer_text="8 м²",
        answer_value=8.0,
        answer_label="Площадь коридора, м²",
        draw=draw_C2,
    )
)


def draw_C3(ax):
    setup_axes(ax)
    # К1 4×4, К2 3×3 над ней (левый край общий); справа коридор 2×7
    draw_rect(ax, 1, 1, 4, 4, "К1(4)", zorder=3)
    draw_rect(ax, 1, 5, 3, 3, "К2(3)", zorder=3)
    draw_rect(ax, 5, 1, 2, 7, "Кор", fc=CORRIDOR, zorder=2)
    draw_dim_v(ax, 1, 8, 0.55, "7 м")
    draw_dim_h(ax, 5, 7, 0.45, "2 м")


problems.append(
    Problem(
        id="C3",
        lvl="Средний",
        title="С3. Две комнаты и узкий коридор",
        text="Комната 1 — квадрат с периметром 16 м. Над ней квадратная комната 2 с периметром 12 м "
        "(стороны выровнены по левому краю, как на плане). Справа — коридор шириной 2 м на всю высоту "
        "квартиры. Найдите площадь коридора.",
        steps=[
            "Сторона К1: 16 : 4 = 4 м.",
            "Сторона К2: 12 : 4 = 3 м.",
            "Высота квартиры слева: 4 + 3 = 7 м — это высота коридора.",
            "Площадь коридора: S = 2 · 7 = 14 м².",
        ],
        answer_text="14 м²",
        answer_value=14.0,
        answer_label="Площадь коридора, м²",
        draw=draw_C3,
    )
)


def draw_C4(ax):
    setup_axes(ax)
    # К1 6×6, К2 4×4; справа сверху 5×4, снизу коридор 5×6
    draw_rect(ax, 1, 1, 6, 6, "К1(6)", zorder=3)
    draw_rect(ax, 1, 7, 6, 4, "К2(4)", zorder=3)
    draw_rect(ax, 7, 7, 5, 4, "К3", zorder=3)
    draw_rect(ax, 7, 1, 5, 6, "Кор", fc=CORRIDOR, zorder=2)
    draw_dim_v(ax, 1, 11, 0.55, "10 м")
    draw_dim_h(ax, 7, 12, 0.45, "5 м")


problems.append(
    Problem(
        id="C4",
        lvl="Средний",
        title="С4. Две комнаты слева и блок справа",
        text="Комната 1 — квадрат с периметром 24 м. Над ней квадратная комната 2 с периметром 16 м. "
        "Справа сверху прямоугольная комната 3 размером 5×4 м, под ней — коридор на всю ширину 5 м. "
        "Высота всей квартиры 10 м. Найдите площадь коридора.",
        steps=[
            "Сторона К1: 24 : 4 = 6 м.",
            "Сторона К2: 16 : 4 = 4 м.",
            "Высота слева: 6 + 4 = 10 м — совпадает с условием.",
            "Комната 3 высотой 4 м, значит под ней коридор высотой 10 − 4 = 6 м.",
            "Площадь коридора: S = 5 · 6 = 30 м².",
        ],
        answer_text="30 м²",
        answer_value=30.0,
        answer_label="Площадь коридора, м²",
        draw=draw_C4,
    )
)


def draw_C5(ax):
    setup_axes(ax)
    draw_rect(ax, 1, 1, 6, 6, "К1(6)", zorder=3)
    draw_rect(ax, 1, 7, 6, 4, "К2(4)", zorder=3)
    draw_rect(ax, 7, 7, 6, 4, "К3", zorder=3)
    draw_rect(ax, 7, 1, 6, 6, "Кор", fc=CORRIDOR, zorder=2)
    draw_dim_v(ax, 1, 11, 0.55, "10 м")
    draw_dim_h(ax, 7, 13, 0.45, "6 м")


problems.append(
    Problem(
        id="C5",
        lvl="Средний",
        title="С5. Коридор и комната 3",
        text="Комната 1 — квадрат со стороной 6 м. Над ней квадратная комната 2 со стороной 4 м. "
        "Справа от комнаты 1 и комнаты 2 расположены два прямоугольника одинаковой ширины: "
        "верхний — комната 3 (6×4 м), нижний — коридор. Высота всей квартиры 10 м. "
        "Найдите площадь коридора.",
        steps=[
            "Высота слева: 6 + 4 = 10 м — совпадает с общей высотой.",
            "Комната 3 высотой 4 м, значит под ней остаётся 10−4=6 м — высота коридора.",
            "Ширина коридора = 6 м.",
            "Площадь коридора: S = 6 · 6 = 36 м².",
        ],
        answer_text="36 м²",
        answer_value=36.0,
        answer_label="Площадь коридора, м²",
        draw=draw_C5,
    )
)


def draw_C6(ax):
    setup_axes(ax)
    draw_rect(ax, 1, 1, 3, 3, "К1(3)", zorder=3)
    draw_rect(ax, 1, 4, 5, 5, "К2(5)", zorder=3)
    draw_rect(ax, 6, 1, 2, 8, "Кор", fc=CORRIDOR, zorder=2)
    draw_dim_v(ax, 1, 9, 0.55, "8 м")
    draw_dim_h(ax, 6, 8, 0.45, "2 м")


problems.append(
    Problem(
        id="C6",
        lvl="Средний",
        title="С6. Периметры 12 м и 20 м",
        text="Нижняя левая комната — квадрат с периметром 12 м. Над ней квадратная комната 2 с периметром "
        "20 м (общий левый край, ширина колонки 5 м, как на плане). Справа коридор шириной 2 м на всю "
        "высоту квартиры. Найдите площадь коридора.",
        steps=[
            "Сторона К1: 12 : 4 = 3 м.",
            "Сторона К2: 20 : 4 = 5 м.",
            "Высота квартиры: 3 + 5 = 8 м.",
            "Площадь коридора: S = 2 · 8 = 16 м².",
        ],
        answer_text="16 м²",
        answer_value=16.0,
        answer_label="Площадь коридора, м²",
        draw=draw_C6,
    )
)


def draw_C7(ax):
    setup_axes(ax)
    draw_rect(ax, 1, 1, 4, 4, "К1(4)", zorder=3)
    draw_rect(ax, 1, 5, 2, 2, "К2(2)", zorder=3)
    draw_rect(ax, 5, 1, 3, 6, "Кор", fc=CORRIDOR, zorder=2)
    draw_dim_v(ax, 1, 7, 0.55, "6 м")
    draw_dim_h(ax, 5, 8, 0.45, "3 м")


problems.append(
    Problem(
        id="C7",
        lvl="Средний",
        title="С7. Маленькая комната сверху",
        text="Комната 1 — квадрат с периметром 16 м. Над ней квадратная комната 2 с периметром 8 м "
        "(левый нижний угол комнаты 2 совпадает с левым верхним углом комнаты 1). Справа коридор "
        "шириной 3 м на всю высоту квартиры. Найдите площадь коридора.",
        steps=[
            "Сторона К1: 16 : 4 = 4 м.",
            "Сторона К2: 8 : 4 = 2 м.",
            "Высота квартиры: 4 + 2 = 6 м.",
            "Площадь коридора: S = 3 · 6 = 18 м².",
        ],
        answer_text="18 м²",
        answer_value=18.0,
        answer_label="Площадь коридора, м²",
        draw=draw_C7,
    )
)


def draw_C8(ax):
    setup_axes(ax)
    draw_rect(ax, 1, 1, 5, 5, "К1(5)", zorder=3)
    draw_rect(ax, 1, 6, 4, 4, "К2(4)", zorder=3)
    draw_rect(ax, 6, 6, 5, 5, "К3(5)", zorder=3)
    draw_rect(ax, 6, 1, 5, 4, "Кор", fc=CORRIDOR, zorder=2)
    draw_dim_v(ax, 1, 10, 0.55, "9 м")
    draw_dim_h(ax, 6, 11, 0.45, "5 м")


problems.append(
    Problem(
        id="C8",
        lvl="Средний",
        title="С8. Три квадрата в два столбца",
        text="Комната 1 — квадрат со стороной 5 м. Над ней квадратная комната 2 со стороной 4 м. "
        "Справа сверху квадратная комната 3 со стороной 5 м, под ней — коридор на всю ширину 5 м. "
        "Найдите площадь коридора.",
        steps=[
            "Высота слева: 5 + 4 = 9 м — общая высота квартиры.",
            "Комната 3 со стороной 5 м занимает верхние 5 м справа, под ней остаётся 9 − 5 = 4 м — высота коридора.",
            "Площадь коридора: S = 5 · 4 = 20 м².",
        ],
        answer_text="20 м²",
        answer_value=20.0,
        answer_label="Площадь коридора, м²",
        draw=draw_C8,
    )
)


def draw_C9(ax):
    setup_axes(ax)
    draw_rect(ax, 1, 1, 5, 5, "К1(5)", zorder=3)
    draw_rect(ax, 1, 6, 3, 3, "К2(3)", zorder=3)
    draw_rect(ax, 6, 1, 4, 8, "Кор", fc=CORRIDOR, zorder=2)
    draw_dim_v(ax, 1, 9, 0.55, "8 м")
    draw_dim_h(ax, 6, 10, 0.45, "4 м")


problems.append(
    Problem(
        id="C9",
        lvl="Средний",
        title="С9. Два столбца разной ширины",
        text="Комната 1 — квадрат с периметром 20 м. Над ней квадратная комната 2 с периметром 12 м "
        "(как на плане). Справа — коридор шириной 4 м на всю высоту квартиры. Найдите площадь коридора.",
        steps=[
            "Сторона К1: 20 : 4 = 5 м.",
            "Сторона К2: 12 : 4 = 3 м.",
            "Высота квартиры: 5 + 3 = 8 м.",
            "Площадь коридора: S = 4 · 8 = 32 м².",
        ],
        answer_text="32 м²",
        answer_value=32.0,
        answer_label="Площадь коридора, м²",
        draw=draw_C9,
    )
)


def draw_C10(ax):
    setup_axes(ax)
    draw_rect(ax, 1, 1, 5, 5, "К1(5)", zorder=3)
    draw_rect(ax, 1, 6, 4, 4, "К2(4)", zorder=3)
    draw_rect(ax, 6, 6, 6, 3, "К3", zorder=3)
    draw_rect(ax, 6, 1, 6, 6, "Кор", fc=CORRIDOR, zorder=2)
    draw_dim_v(ax, 1, 10, 0.55, "9 м")
    draw_dim_h(ax, 6, 12, 0.45, "6 м")


problems.append(
    Problem(
        id="C10",
        lvl="Средний",
        title="С10. Прямоугольник и коридор",
        text="Комната 1 — квадрат со стороной 5 м. Над ней квадратная комната 2 со стороной 4 м. "
        "Справа сверху прямоугольная комната 3 размером 6×3 м, под ней — коридор на всю ширину 6 м. "
        "Найдите площадь коридора.",
        steps=[
            "Высота слева: 5 + 4 = 9 м — общая высота квартиры.",
            "Комната 3 высотой 3 м, значит высота коридора: 9 − 3 = 6 м.",
            "Ширина коридора 6 м.",
            "Площадь коридора: S = 6 · 6 = 36 м².",
        ],
        answer_text="36 м²",
        answer_value=36.0,
        answer_label="Площадь коридора, м²",
        draw=draw_C10,
    )
)

# === ПРОДВИНУТЫЙ УРОВЕНЬ: П1–П5 ===


def draw_P1(ax):
    # Числовой пример a1=6 м: квадраты 6×6, 8×8 и 12×12; коридор 12×2
    setup_axes(ax, xmax=22, ymax=16)
    draw_rect(ax, 1, 1, 6, 6, "a1=6", zorder=3)
    draw_rect(ax, 1, 7, 8, 8, "a2=8", zorder=3)
    draw_rect(ax, 9, 3, 12, 12, "a3=12", zorder=3)
    draw_rect(ax, 9, 1, 12, 2, "Кор", fc=CORRIDOR_ROSE, zorder=4)


problems.append(
    Problem(
        id="P1",
        lvl="Продвинутый",
        title="П1. Выражение через P1",
        text="Комната 1 — квадрат, её периметр P1. Над ней квадратная комната 2, периметр которой на 8 м больше. "
        "Справа квадратная комната 3, её периметр на 16 м больше, чем у комнаты 2. "
        "Под комнатой 3 — коридор. Выразите площадь коридора через P1. (На чертеже — пример при a1 = 6 м.)",
        steps=[
            "Пусть сторона комнаты 1: a1 = P1 / 4.",
            "Тогда a2 = a1 + 2, a3 = a2 + 4 = a1 + 6.",
            "Высота слева: a1 + a2 = 2a1 + 2.",
            "Высота коридора: (2a1 + 2) − (a1 + 6) = a1 − 4.",
            "Ширина коридора: a3 = a1 + 6.",
            "Площадь коридора: S = (a1 − 4)(a1 + 6).",
        ],
        answer_text="S = (a1 − 4)(a1 + 6)",
        answer_value=0.0,
        answer_label="(для этой задачи проверь себя по решению ниже)",
        draw=draw_P1,
    )
)


def draw_P2(ax):
    setup_axes(ax)
    draw_rect(ax, 1, 2, 3, 3, "К1(3)", zorder=3)
    draw_rect(ax, 4, 2, 7, 3, "Кор", fc=CORRIDOR, zorder=4)
    draw_rect(ax, 1, 5, 5, 5, "К2(5)", zorder=3)
    draw_rect(ax, 6, 5, 5, 5, "К3(5)", zorder=3)
    draw_rect(ax, 11, 2, 6, 6, "К4(8)", zorder=3)


problems.append(
    Problem(
        id="P2",
        lvl="Продвинутый",
        title="П2. Восстановление плана",
        text="Высота коридора 3 м, его площадь 21 м². Комната 1 — квадрат 3×3, находится внизу слева. "
        "По этим данным восстановите периметры остальных квадратных комнат, если план как на рисунке.",
        steps=[
            "Высота коридора: 3 м, площадь 21 м² → длина коридора 7 м.",
            "Снизу: справа от К1 (3 м) ещё 7 м коридора → всего 10 м.",
            "Сверху над ними две комнаты по 5 м (К2 и К3), их периметры по 20 м.",
            "Правая большая комната К4 имеет сторону 8 м (по рисунку) и периметр 32 м.",
            "Итого периметры: К1 — 12 м, К2 — 20 м, К3 — 20 м, К4 — 32 м.",
        ],
        answer_text="Периметры: 12, 20, 20, 32 м.",
        answer_value=0.0,
        answer_label="(здесь ответ — набор периметров, смотри решение)",
        draw=draw_P2,
    )
)


def draw_P3(ax):
    setup_axes(ax, xmax=20, ymax=14)
    # К1 4×4, К2 6×6; справа коридор 6×4 и К3 6×6; К4 6×10
    draw_rect(ax, 1, 2, 4, 4, "К1(4)", zorder=3)
    draw_rect(ax, 1, 6, 6, 6, "К2(6)", zorder=3)
    draw_rect(ax, 7, 2, 6, 4, "Кор", fc=CORRIDOR, zorder=2)
    draw_rect(ax, 7, 6, 6, 6, "К3(6)", zorder=3)
    draw_rect(ax, 13, 2, 6, 10, "К4(10)", zorder=3)


problems.append(
    Problem(
        id="P3",
        lvl="Продвинутый",
        title="П3. Стороны комнат 2 и 3",
        text="Комната 4 — квадрат, её периметр 40 м. Слева снизу — квадратная комната 1 с периметром 16 м, "
        "над ней квадратная комната 2, справа над коридором — квадратная комната 3. "
        "Найдите стороны комнат 2 и 3 и площадь коридора.",
        steps=[
            "К1: P=16 → a1=4 м. К4: P=40 → a4=10 м.",
            "Высота квартиры 10 м. Тогда сторона К2: a2 = 10 − 4 = 6 м.",
            "Комната 3 — квадрат, возьмём сторону a3 = 6 м.",
            "Коридор под К3: высота 4 м, ширина 6 м.",
            "Площадь коридора: S = 4 · 6 = 24 м².",
        ],
        answer_text="a2=6 м, a3=6 м, S=24 м²",
        answer_value=24.0,
        answer_label="Площадь коридора, м²",
        draw=draw_P3,
    )
)


def draw_P4(ax):
    # Пример a=4 м: квадраты 4×4, 5×5, 7×7; коридор 7×2
    setup_axes(ax, xmax=15, ymax=12)
    draw_rect(ax, 1, 1, 4, 4, "a=4", zorder=3)
    draw_rect(ax, 1, 5, 5, 5, "a+1=5", zorder=3)
    draw_rect(ax, 6, 3, 7, 7, "a+3=7", zorder=3)
    draw_rect(ax, 6, 1, 7, 2, "Кор", fc=CORRIDOR_ROSE, zorder=4)


problems.append(
    Problem(
        id="P4",
        lvl="Продвинутый",
        title="П4. Переменная a",
        text="Комната 1 — квадрат, её сторона a метров. Над ней квадратная комната 2 со стороной a+1 м. "
        "Справа от комнаты 2 — квадратная комната 3 со стороной a+3 м, под ней — коридор. "
        "Общая высота квартиры равна 2a+1 м. Найдите площадь коридора через a. (На чертеже — пример при a = 4 м.)",
        steps=[
            "Высота слева: a + (a+1) = 2a+1 — совпадает с общей высотой.",
            "Справа: комната 3 высотой a+3.",
            "Высота коридора: (2a+1) − (a+3) = a−2.",
            "Ширина коридора: a+3.",
            "Площадь: S = (a−2)(a+3).",
        ],
        answer_text="S = (a−2)(a+3)",
        answer_value=0.0,
        answer_label="(ответ — выражение, смотри решение)",
        draw=draw_P4,
    )
)


def draw_P5(ax):
    setup_axes(ax)
    draw_rect(ax, 5, 1, 8, 3, "Кор", fc=CORRIDOR, zorder=4)
    draw_rect(ax, 1, 1, 3, 3, "К1(3)", zorder=3)
    draw_rect(ax, 1, 4, 4, 4, "К2(4)", zorder=3)
    draw_rect(ax, 5, 1, 8, 8, "К3(8)", zorder=2)


problems.append(
    Problem(
        id="P5",
        lvl="Продвинутый",
        title="П5. Три квадрата и коридор",
        text="В квартире три квадратные комнаты и коридор. Нижняя левая комната имеет периметр 12 м, "
        "верхняя левая — периметр 16 м, правая — периметр 32 м. Коридор занимает нижнее правое место "
        "и его высота равна высоте нижней левой комнаты. Найдите площадь коридора.",
        steps=[
            "Нижняя левая: P=12 → сторона 3 м.",
            "Верхняя левая: P=16 → сторона 4 м.",
            "Правая комната: P=32 → сторона 8 м.",
            "Высота коридора = 3 м, ширина = 8 м.",
            "Площадь коридора: S = 3 · 8 = 24 м².",
        ],
        answer_text="24 м²",
        answer_value=24.0,
        answer_label="Площадь коридора, м²",
        draw=draw_P5,
    )
)


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

    _stats = st.session_state["stats"]
    _rate_txt = ""
    if _stats["attempts"] > 0:
        _rate_txt = f" · верно {_stats['success'] / _stats['attempts'] * 100:.0f}%"
    st.caption(
        f"Статистика за сеанс: попыток — {_stats['attempts']}, "
        f"верных — {_stats['success']}{_rate_txt}"
    )

    st.markdown("---")

    col_left, col_right = st.columns([1, 2], gap="small", vertical_alignment="top")

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
            st.caption(f"Уровень: {problem.lvl}")

            st.markdown("**Чертёж**")
            fig, ax = plt.subplots(figsize=(4.8, 3.6), dpi=130)
            problem.draw(ax)
            fig.patch.set_facecolor("white")
            buf = io.BytesIO()
            fig.savefig(
                buf,
                format="png",
                bbox_inches="tight",
                pad_inches=0.05,
                facecolor="white",
                edgecolor="none",
            )
            plt.close(fig)
            buf.seek(0)
            st.image(buf, width=520)

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
                    key=f"answer_{problem.id}",
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
