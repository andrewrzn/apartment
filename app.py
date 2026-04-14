import streamlit as st
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Callable, Dict, Any, Optional

st.set_page_config(
    page_title="Геометрия квартиры: 5 класс",
    page_icon="📐",
    layout="wide"
)

# ---------- МОДЕЛЬ ЗАДАЧ ----------

@dataclass
class Problem:
    id: str
    lvl: str
    title: str
    text: str
    steps: List[str]
    answer_text: str        # строка для вывода
    answer_value: float     # численное значение для проверки (например, площадь)
    answer_label: str       # как называется ответ (например: "Площадь коридора, м²")
    draw: Callable[[plt.Axes], None]


# ---------- ДАННЫЕ ДЛЯ ТЕОРИИ ----------

theory_cards = [
    ("🔲", "Квадрат", "Периметр квадрата: P = 4·a. Чтобы найти сторону: a = P / 4."),
    ("▭", "Прямоугольник", "Площадь: S = a·b (длина на ширину)."),
    ("🧩", "План квартиры", "Общая высота/ширина квартиры — это сумма высот/ширин всех комнат и коридора."),
]


# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ РИСОВАНИЯ ----------

def draw_rect(ax: plt.Axes, x: float, y: float, w: float, h: float, label: str = "",
              fc: str = "#ffffff", ec: str = "#000000"):
    ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=2))
    if label:
        ax.text(x + w / 2, y + h / 2, label,
                ha="center", va="center", fontsize=10)


def draw_dim_h(ax: plt.Axes, x1, x2, y, text):
    ax.plot([x1, x2], [y, y], color="#dd6b20", linewidth=1)
    ax.text((x1 + x2) / 2, y + 0.2, text, ha="center", va="bottom",
            fontsize=9, color="#dd6b20")


def draw_dim_v(ax: plt.Axes, y1, y2, x, text):
    ax.plot([x, x], [y1, y2], color="#dd6b20", linewidth=1)
    ax.text(x - 0.2, (y1 + y2) / 2, text, ha="right", va="center",
            fontsize=9, color="#dd6b20", rotation="vertical")


# ---------- ОПРЕДЕЛЕНИЕ ЗАДАЧ (пока базовый+1 средний+1 продвинутый) ----------

problems: List[Problem] = []

# Б1
def draw_B1(ax: plt.Axes):
    ax.set_aspect("equal")
    # Комната 4×4
    draw_rect(ax, 0, 0, 4, 4, "Комната", fc="#dcfce7")
    # Коридор 4×6 справа
    draw_rect(ax, 4, 0, 6, 4, "Коридор", fc="#e0f2fe")
    draw_dim_v(ax, 0, 4, -0.3, "4 м")
    draw_dim_h(ax, 4, 10, -0.5, "6 м")
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 6)
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
def draw_B2(ax: plt.Axes):
    ax.set_aspect("equal")
    # Комната 5×5
    draw_rect(ax, 0, 0, 5, 5, "Комната", fc="#ffffff")
    # Балкон 5×2 сверху
    draw_rect(ax, 0, 5, 5, 2, "Балкон", fc="#ffedd5")
    draw_dim_h(ax, 0, 5, -0.5, "5 м")
    draw_dim_v(ax, 5, 7, 5.3, "2 м")
    ax.set_xlim(-1, 7)
    ax.set_ylim(-1, 8)
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
def draw_B3(ax: plt.Axes):
    ax.set_aspect("equal")
    # Комната 3×3 справа
    draw_rect(ax, 2, 0, 3, 3, "К1", fc="#ffffff")
    # Коридор слева 2×3
    draw_rect(ax, 0, 0, 2, 3, "Коридор", fc="#e0f2fe")
    draw_dim_h(ax, 0, 2, -0.5, "2 м")
    draw_dim_v(ax, 0, 3, 4.5, "3 м")
    ax.set_xlim(-1, 6)
    ax.set_ylim(-1, 5)
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
def draw_B4(ax: plt.Axes):
    ax.set_aspect("equal")
    # Комната 6×6
    draw_rect(ax, 0, 0, 6, 6, "Комната", fc="#ffffff")
    # Коридор вдоль справа 3×6
    draw_rect(ax, 6, 0, 3, 6, "Коридор", fc="#e0f2fe")
    draw_dim_h(ax, 0, 6, -0.5, "6 м")
    draw_dim_h(ax, 6, 9, -0.5, "3 м")
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 7)
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
def draw_B5(ax: plt.Axes):
    ax.set_aspect("equal")
    # Две комнаты 4×4 слева
    draw_rect(ax, 0, 0, 4, 4, "К1", fc="#dcfce7")
    draw_rect(ax, 0, 4, 4, 4, "К2", fc="#dcfce7")
    # Коридор 2×8 справа
    draw_rect(ax, 4, 0, 2, 8, "Коридор", fc="#e0f2fe")
    draw_dim_v(ax, 0, 8, -0.3, "8 м")
    draw_dim_h(ax, 4, 6, -0.5, "2 м")
    ax.set_xlim(-1, 7)
    ax.set_ylim(-1, 9)
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

# Можно дальше аналогично добавить C1, C2, P1 и т.д.


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
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.subheader("Сложность")
        levels = ["Базовый", "Средний", "Продвинутый"]
        current_level = st.radio("Выберите уровень", levels)

        st.subheader("Выбор задачи")
        filtered = [p for p in problems if p.lvl == current_level]
        if not filtered:
            st.info("Для этого уровня задачи пока не добавлены.")
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

            fig, ax = plt.subplots(figsize=(5, 4))
            problem.draw(ax)
            st.pyplot(fig)

            st.markdown("#### Условие")
            st.write(problem.text)

            st.markdown("#### Попробуй решить сам")

            user_value = st.number_input(
                problem.answer_label,
                value=0.0,
                step=1.0,
                format="%.1f"
            )

            col_check1, col_check2 = st.columns([1, 2])
            with col_check1:
                check = st.button("Проверить ответ")

            if check:
                if abs(user_value - problem.answer_value) < 1e-6:
                    st.success("Отлично! Ответ верный 🎉")
                    st.balloons()
                else:
                    st.error("Пока неверно. Посмотри решение ниже и попробуй ещё раз.")

            show_solution = st.toggle("Показать решение", value=False)
            if show_solution:
                st.markdown("#### Пошаговое решение")
                for i, step in enumerate(problem.steps, start=1):
                    st.markdown(f"**{i}.** {step}")
                st.markdown(f"**Ответ:** {problem.answer_text}")
