import streamlit as st
from streamlit_drawable_canvas import st_canvas
from dataclasses import dataclass
from typing import Callable, List, Dict

st.set_page_config(
    page_title="Геометрия квартиры: 5 класс",
    page_icon="📐",
    layout="wide"
)

st.markdown(
    """
    <style>
    body { background-color: #faf8f5; }
    .main { background-color: #faf8f5; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- ОПИСАНИЕ СТРУКТУР ----------

@dataclass
class Problem:
    id: str
    lvl: str
    title: str
    text: str
    steps: List[str]
    answer: str
    draw: Callable  # функция рисования


# ---------- ДАННЫЕ ДЛЯ ТЕОРИИ ----------

theory_cards = [
    ("🔲", "Квадрат", "P = 4·a. Все стороны равны. Чтобы найти сторону, раздели периметр на 4."),
    ("▭", "Прямоугольник", "S = a·b. Площадь — это произведение длины на ширину."),
    ("🧩", "Составные фигуры", "Общая высота или ширина складывается из частей соседних комнат."),
]


# ---------- ФУНКЦИИ РИСОВАНИЯ НА CANVAS ----------

def draw_rect(canvas, x, y, w, h, label="", fill_color="#ffffff", stroke_color="#000000"):
    canvas.rect(
        x, y, w, h,
        fill_color=fill_color,
        stroke_color=stroke_color,
        stroke_width=2
    )
    if label:
        canvas.text(
            x + w / 2,
            y + h / 2,
            label,
            color="#2d3748",
            font_size=16,
            align="center",
        )


def draw_dim(canvas, x1, y1, x2, y2, text, vertical=False):
    """Очень упрощённая «размерная» линия."""
    color = "#dd6b20"
    if vertical:
        canvas.line(x1, y1, x1, y2, stroke_color=color, stroke_width=1.5)
        canvas.text(x1 - 10, (y1 + y2) / 2, text, color=color, font_size=14, align="right")
    else:
        canvas.line(x1, y1, x2, y1, stroke_color=color, stroke_width=1.5)
        canvas.text((x1 + x2) / 2, y1 + 15, text, color=color, font_size=14, align="center")


# ---------- ЗАДАЧИ ----------

problems: List[Problem] = []

# Базовый уровень
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
        "S = 4 · 6 = 24 м²."
    ],
    answer="24 м²",
    draw=lambda c: (
        draw_rect(c, 50, 100, 120, 120, "Комната", "#dcfce7"),
        draw_rect(c, 170, 100, 180, 120, "Коридор", "#e0f2fe"),
        draw_dim(c, 50, 230, 50, 100, "4 м", vertical=True),
        draw_dim(c, 170, 230, 350, 230, "6 м", vertical=False),
    )
))

problems.append(Problem(
    id="B2",
    lvl="Базовый",
    title="Б2. Балкон",
    text="Квадратная комната имеет периметр 20 м. По одной стороне комнаты сделан прямоугольный "
         "балкон шириной 2 м и такой же длины, как сторона комнаты. Найдите площадь балкона.",
    steps=[
        "Сторона комнаты: 20 : 4 = 5 м.",
        "Длина балкона = 5 м, ширина = 2 м.",
        "S = 5 · 2 = 10 м²."
    ],
    answer="10 м²",
    draw=lambda c: (
        draw_rect(c, 150, 150, 150, 150, "Комната", "#ffffff"),
        draw_rect(c, 150, 100, 150, 50, "Балкон", "#ffedd5"),
        draw_dim(c, 150, 305, 300, 305, "5 м", vertical=False),
        draw_dim(c, 305, 100, 305, 150, "2 м", vertical=True),
    )
))

problems.append(Problem(
    id="B3",
    lvl="Базовый",
    title="Б3. Коридор слева",
    text="Комната 1 — квадрат с периметром 12 м. Слева от неё находится прямоугольный коридор "
         "длиной 2 м и такой же высоты, как комната. Найдите площадь коридора.",
    steps=[
        "Сторона комнаты: 12 : 4 = 3 м.",
        "Коридор: высота 3 м, длина 2 м.",
        "S = 3 · 2 = 6 м²."
    ],
    answer="6 м²",
    draw=lambda c: (
        draw_rect(c, 150, 120, 80, 120, "Кор.", "#f3f4f6"),
        draw_rect(c, 230, 120, 120, 120, "Комната 1", "#ffffff"),
        draw_dim(c, 150, 245, 230, 245, "2 м", vertical=False),
        draw_dim(c, 350, 120, 350, 240, "3 м", vertical=True),
    )
))

problems.append(Problem(
    id="B4",
    lvl="Базовый",
    title="Б4. Коридор вдоль стороны",
    text="Квадратная комната имеет периметр 24 м. Вдоль одной её стороны проходит коридор шириной "
         "3 м и длиной, равной стороне комнаты. Найдите площадь коридора.",
    steps=[
        "Сторона комнаты: 24 : 4 = 6 м.",
        "Коридор: 6 м × 3 м.",
        "S = 18 м²."
    ],
    answer="18 м²",
    draw=lambda c: (
        draw_rect(c, 150, 100, 180, 180, "Комната", "#ffffff"),
        draw_rect(c, 330, 100, 90, 180, "Кор.", "#e0f2fe"),
        draw_dim(c, 150, 285, 330, 285, "6 м", vertical=False),
        draw_dim(c, 330, 285, 420, 285, "3 м", vertical=False),
    )
))

problems.append(Problem(
    id="B5",
    lvl="Базовый",
    title="Б5. Две комнаты и коридор",
    text="Комната 1 и Комната 2 — квадраты 4×4 м. Справа — прямоугольный коридор высотой 8 м и "
         "шириной 2 м. Найдите площадь коридора.",
    steps=[
        "Общая высота слева: 4 + 4 = 8 м.",
        "Коридор: 8 м × 2 м.",
        "S = 16 м²."
    ],
    answer="16 м²",
    draw=lambda c: (
        draw_rect(c, 150, 180, 100, 100, "№1", "#dcfce7"),
        draw_rect(c, 150, 80, 100, 100, "№2", "#dcfce7"),
        draw_rect(c, 250, 80, 60, 200, "Коридор", "#e0f2fe"),
        draw_dim(c, 310, 80, 310, 280, "8 м", vertical=True),
        draw_dim(c, 250, 285, 310, 285, "2 м", vertical=False),
    )
))

# Средний и продвинутый — для примера добавим по одной-две задачи
# (ты можешь перенести сюда остальные по аналогии).

problems.append(Problem(
    id="C1",
    lvl="Средний",
    title="С1. Три комнаты",
    text="Комната 1 — квадрат с периметром 16 м, снизу слева. Над ней комната 2 со стороной 6 м. "
         "Справа квадратная комната 3, высота всей квартиры 10 м. Под комнатой 3 — коридор. "
         "Найдите сторону комнаты 1, сторону комнаты 3 и площадь коридора.",
    steps=[
        "Сторона комнаты 1: 16 : 4 = 4 м.",
        "Высота слева: 4 + 6 = 10 м, значит сторона комнаты 3 = 10 м.",
        "Коридор под комнатой 3: высота 10 − 4 = 6 м, ширина 10 м.",
        "S = 6 · 10 = 60 м²."
    ],
    answer="60 м²",
    draw=lambda c: (
        draw_rect(c, 80, 200, 80, 80, "К1 (4)", "#ffffff"),
        draw_rect(c, 80, 120, 80, 80, "К2 (6)", "#ffffff"),
        draw_rect(c, 160, 120, 120, 160, "К3 (10)", "#ffffff"),
        draw_rect(c, 160, 280, 120, 40, "Коридор", "#e2e8f0"),
        draw_dim(c, 80, 280, 80, 120, "10 м", vertical=True),
    )
))

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
        "S = (a1 − 4)(a1 + 6)."
    ],
    answer="S = (a1 − 4)(a1 + 6)",
    draw=lambda c: (
        draw_rect(c, 100, 220, 80, 80, "a1", "#ffffff"),
        draw_rect(c, 100, 120, 80, 100, "a2", "#ffffff"),
        draw_rect(c, 180, 120, 150, 150, "a3", "#ffffff"),
        draw_rect(c, 180, 270, 150, 30, "S", "#fee2e2"),
    )
))


# ---------- UI ----------

st.title("📐 Геометрия квартиры: 5 класс")
st.markdown("Интерактивное пособие по задачам на план квартиры и площадь коридора.")

tab_theory, tab_practice = st.tabs(["Правила", "Задачи"])

with tab_theory:
    st.subheader("Наши инструменты")
    cols = st.columns(len(theory_cards))
    for col, (icon, title, desc) in zip(cols, theory_cards):
        with col:
            st.markdown(f"### {icon} {title}")
            st.write(desc)

with tab_practice:
    # Левая колонка — выбор уровня и задачи
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.subheader("Сложность")
        levels = ["Базовый", "Средний", "Продвинутый"]
        current_level = st.radio(
            "Выберите уровень",
            levels,
            label_visibility="collapsed"
        )

        # Список задач
        st.subheader("Список задач")
        filtered = [p for p in problems if p.lvl == current_level]
        titles = [p.title for p in filtered]
        if not titles:
            st.info("Для этого уровня задачи пока не добавлены.")
            selected_title = None
        else:
            selected_title = st.radio(
                "Выберите задачу",
                titles,
                index=0,
                label_visibility="collapsed"
            )

    with col_right:
        if not filtered or selected_title is None:
            st.info("Выберите задачу слева, чтобы увидеть условие и чертёж.")
        else:
            problem = next(p for p in filtered if p.title == selected_title)

            st.markdown(f"#### {problem.title}")
            st.markdown(f"**Уровень:** {problem.lvl}")

            st.markdown("##### Чертёж")
            canvas_result = st_canvas(
                fill_color="rgba(0, 0, 0, 0)",  # прозрачная заливка по умолчанию
                stroke_width=1,
                background_color="#ffffff",
                height=350,
                width=600,
                drawing_mode="transform",  # пользователь не рисует сам
                key=f"canvas_{problem.id}",
            )

            # Рисуем поверх canvas через "начальное состояние"
            # streamlit-drawable-canvas не даёт просто так императивно рисовать,
            # поэтому для реального рендера фигур лучше использовать st.pyplot / matplotlib.
            # Для простоты сейчас покажем текстовое описание вместо живого рисования.
            st.caption("В этой демо-версии чертёж описан словами. "
                       "При желании можно заменить на matplotlib для точного рисунка.")

            st.markdown("##### Условие")
            st.write(problem.text)

            show_solution = st.toggle("Показать решение", value=False)
            if show_solution:
                st.markdown("##### Пошаговый разбор")
                for i, step in enumerate(problem.steps, start=1):
                    st.markdown(f"**{i}.** {step}")
                st.markdown(f"#### Ответ: {problem.answer}")
