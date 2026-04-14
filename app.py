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
    answer_value: float     # числовой ответ (например, площадь)
    answer_label: str       # подпись к полю ввода (что именно вводим)
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
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=9)


def draw_dim_h(ax: plt.Axes, x1, x2, y, text):
    ax.plot([x1, x2], [y, y], color="#dd6b20", linewidth=1)
    ax.text((x1 + x2) / 2, y - 0.2, text, ha="center", va="top", fontsize=9, color="#dd6b20")


def draw_dim_v(ax: plt.Axes, y1, y2, x, text):
    ax.plot([x, x], [y1, y2], color="#dd6b20", linewidth=1)
    ax.text(x - 0.2, (y1 + y2) / 2, text, ha="right", va="center", fontsize=9, color="#dd6b20",
            rotation="vertical")


# ---------- ОПРЕДЕЛЕНИЕ ЗАДАЧ ----------

problems: List[Problem] = []

# === БАЗОВЫЙ УРОВЕНЬ ===

# Б1
def draw_B1(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 0, 0, 4, 4, "Комната", "#dcfce7")
    draw_rect(ax, 4, 0, 6, 4, "Коридор", "#e0f2fe")
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
def draw_B2(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 0, 0, 5, 5, "Комната", "#ffffff")
    draw_rect(ax, 0, 5, 5, 2, "Балкон", "#ffedd5")
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
def draw_B3(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 2, 0, 3, 3, "К1", "#ffffff")
    draw_rect(ax, 0, 0, 2, 3, "Коридор", "#e0f2fe")
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
def draw_B4(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 0, 0, 6, 6, "Комната", "#ffffff")
    draw_rect(ax, 6, 0, 3, 6, "Коридор", "#e0f2fe")
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
def draw_B5(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 0, 0, 4, 4, "К1", "#dcfce7")
    draw_rect(ax, 0, 4, 4, 4, "К2", "#dcfce7")
    draw_rect(ax, 4, 0, 2, 8, "Коридор", "#e0f2fe")
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

# === СРЕДНИЙ УРОВЕНЬ (пример: C1, C2) ===

def draw_C1(ax):
    ax.set_aspect("equal")
    # К1: 4x4 внизу слева
    draw_rect(ax, 0, 0, 4, 4, "К1(4)", "#ffffff")
    # К2: 6x6 над ней
    draw_rect(ax, 0, 4, 4, 6, "К2(6)", "#ffffff")
    # К3: 10x10 справа
    draw_rect(ax, 4, 0, 10, 10, "К3(10)", "#ffffff")
    # Коридор под К3 (10x6)
    draw_rect(ax, 4, 0, 10, 6, "", "#e0f2fe")
    draw_dim_v(ax, 0, 10, -0.5, "10 м")
    draw_dim_h(ax, 4, 14, -0.5, "10 м")
    ax.set_xlim(-2, 16)
    ax.set_ylim(-1, 11)
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

def draw_C2(ax):
    ax.set_aspect("equal")
    # К1 4x4
    draw_rect(ax, 0, 0, 4, 4, "К1(4)", "#ffffff")
    # К2 3x3 над К1
    draw_rect(ax, 0, 4, 4, 3, "К2(3)", "#ffffff")
    # К4 7x7 справа
    draw_rect(ax, 4, 0, 7, 7, "К4(7)", "#ffffff")
    # К3 3x3 над коридором
    draw_rect(ax, 4, 4, 3, 3, "К3(3)", "#ffffff")
    # Коридор 2x4 под К3
    draw_rect(ax, 4, 0, 2, 4, "Кор", "#e0f2fe")
    draw_dim_h(ax, 4, 6, -0.5, "2 м")
    draw_dim_v(ax, 0, 4, 6.2, "4 м")
    ax.set_xlim(-2, 12)
    ax.set_ylim(-1, 8)
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

# === ПРОДВИНУТЫЙ УРОВЕНЬ (пример: P1) ===

def draw_P1(ax):
    ax.set_aspect("equal")
    draw_rect(ax, 0, 0, 3, 3, "a1", "#ffffff")
    draw_rect(ax, 0, 3, 3, 4, "a2", "#ffffff")
    draw_rect(ax, 3, 0, 5, 7, "a3", "#ffffff")
    draw_rect(ax, 3, 0, 5, 1, "Кор", "#fee2e2")
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
    answer_value=0.0,  # здесь проверку по числу не делаем
    answer_label="(для этой задачи можно просто смотреть решение)",
    draw=draw_P1
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

        st.subheader("Статистика за сеанс")
        stats = st.session_state["stats"]
        st.write(f"Всего попыток: {stats['attempts']}")
        st.write(f"Удачных попыток: {stats['success']}")
        if stats["attempts"] > 0:
            rate = stats["success"] / stats["attempts"] * 100
            st.write(f"Процент верных ответов: {rate:.1f}%")

    with col_right:
        if not filtered or selected_title is None:
            st.info("Выберите задачу слева.")
        else:
            problem = next(p for p in filtered if p.title == selected_title)

            st.markdown(f"### {problem.title}")
            st.markdown(f"**Уровень:** {problem.lvl}")
            st.markdown("#### Чертёж")

            fig, ax = plt.subplots(figsize=(4, 3))
            problem.draw(ax)
            st.pyplot(fig)

            st.markdown("#### Условие")
            st.write(problem.text)

            # Ввод ответа
            st.markdown("#### Попробуй решить сам")

            # Для продвинутых задач, где ответ выражение, можно не проверять число
            can_check_numeric = problem.answer_value != 0.0

            if can_check_numeric:
                user_value = st.number_input(
                    problem.answer_label,
                    value=0.0,
                    step=1.0,
                    format="%.1f"
                )
                check = st.button("Проверить ответ")
                if check:
                    st.session_state["stats"]["attempts"] += 1
                    if abs(user_value - problem.answer_value) < 1e-6:
                        st.session_state["stats"]["success"] += 1
                        st.success("Отлично! Ответ верный 🎉")
                        st.balloons()
                    else:
                        st.error("Пока неверно. Посмотри решение ниже и попробуй ещё раз.")
            else:
                st.info("Для этой задачи проверь себя по решению ниже (ответ в виде выражения).")

            show_solution = st.toggle("Показать решение", value=False)
            if show_solution:
                st.markdown("#### Пошаговое решение")
                for i, step in enumerate(problem.steps, start=1):
                    st.markdown(f"**{i}.** {step}")
                st.markdown(f"**Ответ:** {problem.answer_text}")
