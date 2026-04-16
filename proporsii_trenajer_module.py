from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Callable
import re

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import streamlit as st


@dataclass
class Task:
    number: int
    level: str
    title: str
    text: str
    answer_text: str
    explanation: str
    expected: tuple[float, ...]
    draw: Callable[[plt.Axes], None]
    multi_input: bool = False
    allow_any_order: bool = True
    bonus_accept_percent: bool = False


def _setup_axis(ax: plt.Axes, w: float = 10, h: float = 6) -> None:
    ax.set_aspect("equal")
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")


def _draw_split(ax: plt.Axes, widths: list[float], labels: list[str], *, height: float = 3.8, y: float = 1.1) -> None:
    total = sum(widths)
    # Нормализуем ширины к единому размеру рисунка, чтобы все схемы были одинаковыми.
    k = 10 / total if total else 1.0
    widths = [w * k for w in widths]
    x = 1.0
    palette = ["#bfdbfe", "#86efac", "#fde68a", "#fecaca"]
    for i, (w, label) in enumerate(zip(widths, labels)):
        ax.add_patch(
            Rectangle(
                (x, y),
                w,
                height,
                facecolor=palette[i % len(palette)],
                edgecolor="#1e293b",
                linewidth=2,
            )
        )
        ax.text(x + w / 2, y + height / 2, label, ha="center", va="center", fontsize=12, weight="bold")
        x += w
    _setup_axis(ax, w=12, h=6)


def _d1(ax: plt.Axes) -> None: _draw_split(ax, [5, 5], ["50 см²", "50 см²"])
def _d2(ax: plt.Axes) -> None: _draw_split(ax, [1, 2], ["20", "40"])
def _d3(ax: plt.Axes) -> None: _draw_split(ax, [1, 3], ["30", "90"])
def _d4(ax: plt.Axes) -> None: _draw_split(ax, [1, 4], ["20", "80"])
def _d5(ax: plt.Axes) -> None: _draw_split(ax, [1, 3], ["40", "120"])
def _d6(ax: plt.Axes) -> None:
    # 8×15 см: короткая сторона 8 см делится 1:3 → 2 см и 6 см, разрез параллелен стороне 15 см.
    h = 15.0
    ax.add_patch(
        Rectangle(
            (0, 0),
            2,
            h,
            facecolor="#bfdbfe",
            edgecolor="#1e293b",
            linewidth=2,
        )
    )
    ax.add_patch(
        Rectangle(
            (2, 0),
            6,
            h,
            facecolor="#86efac",
            edgecolor="#1e293b",
            linewidth=2,
        )
    )
    ax.text(1, h / 2, "30", ha="center", va="center", fontsize=11, weight="bold")
    ax.text(5, h / 2, "90", ha="center", va="center", fontsize=11, weight="bold")
    ax.text(1, -0.9, "2 см", ha="center", va="top", fontsize=10, color="#334155")
    ax.text(5, -0.9, "6 см", ha="center", va="top", fontsize=10, color="#334155")
    ax.text(4, h + 0.6, "15 см", ha="center", va="bottom", fontsize=10, color="#334155")
    ax.set_aspect("equal")
    ax.set_xlim(-0.35, 8.35)
    ax.set_ylim(-1.55, h + 1.15)
    ax.axis("off")


def _d7(ax: plt.Axes) -> None:
    # 10×20 см: длинная сторона 20 см делится 1:4 → 4 см и 16 см, разрез параллелен стороне 10 см.
    w_long = 20.0
    h_short = 10.0
    ax.add_patch(
        Rectangle(
            (0, 0),
            4,
            h_short,
            facecolor="#bfdbfe",
            edgecolor="#1e293b",
            linewidth=2,
        )
    )
    ax.add_patch(
        Rectangle(
            (4, 0),
            16,
            h_short,
            facecolor="#86efac",
            edgecolor="#1e293b",
            linewidth=2,
        )
    )
    ax.text(2, h_short / 2, "40", ha="center", va="center", fontsize=11, weight="bold")
    ax.text(12, h_short / 2, "160", ha="center", va="center", fontsize=11, weight="bold")
    ax.text(2, -0.65, "4 см", ha="center", va="top", fontsize=10, color="#334155")
    ax.text(12, -0.65, "16 см", ha="center", va="top", fontsize=10, color="#334155")
    ax.text(w_long / 2, h_short + 0.55, "20 см (длинная)", ha="center", va="bottom", fontsize=9, color="#334155")
    ax.text(-0.55, h_short / 2, "10 см", ha="right", va="center", fontsize=10, color="#334155")
    ax.set_aspect("equal")
    ax.set_xlim(-1.0, w_long + 0.5)
    ax.set_ylim(-1.25, h_short + 1.05)
    ax.axis("off")
def _d8(ax: plt.Axes) -> None: _draw_split(ax, [2, 3], ["2 части", "3 части"])
def _d9(ax: plt.Axes) -> None:
    # Квадрат 12×12 см: сторона делится 1:3 → 3 см и 9 см.
    s = 12.0
    ax.add_patch(
        Rectangle(
            (0, 0),
            3,
            s,
            facecolor="#bfdbfe",
            edgecolor="#1e293b",
            linewidth=2,
        )
    )
    ax.add_patch(
        Rectangle(
            (3, 0),
            9,
            s,
            facecolor="#86efac",
            edgecolor="#1e293b",
            linewidth=2,
        )
    )
    ax.text(1.5, s / 2, "36", ha="center", va="center", fontsize=11, weight="bold")
    ax.text(7.5, s / 2, "108", ha="center", va="center", fontsize=11, weight="bold")
    ax.text(1.5, -0.75, "3 см", ha="center", va="top", fontsize=10, color="#334155")
    ax.text(7.5, -0.75, "9 см", ha="center", va="top", fontsize=10, color="#334155")
    ax.text(-0.7, s / 2, "12 см", ha="right", va="center", fontsize=10, color="#334155")
    ax.set_aspect("equal")
    ax.set_xlim(-1.15, 12.35)
    ax.set_ylim(-1.35, s + 0.85)
    ax.axis("off")


def _d10(ax: plt.Axes) -> None: _draw_split(ax, [1, 3], ["100", "300"])
def _d11(ax: plt.Axes) -> None: _draw_split(ax, [3, 5], ["60", "100"])
def _d12(ax: plt.Axes) -> None: _draw_split(ax, [50, 250], ["50×50", "остаток"])
def _d13(ax: plt.Axes) -> None: _draw_split(ax, [1, 6], ["20", "120"])
def _d14(ax: plt.Axes) -> None: _draw_split(ax, [2, 1, 3], ["80", "40", "120"])
def _d15(ax: plt.Axes) -> None: _draw_split(ax, [1, 4], ["A", "B"])


TASKS: list[Task] = [
    Task(1, "Уровень 1", "Базовый 1", "Прямоугольник площадью 100 см² разрезали на 2 равные части. Во сколько раз площадь целого больше площади одной части?", "2 раза", "100 ÷ 2 = 50. Целое 100, часть 50, значит в 2 раза.", (2,), _d1),
    Task(2, "Уровень 1", "Базовый 2", "Площадь 60 см², одна часть в 2 раза больше другой. Найдите площади обеих частей (введите через запятую).", "20 см² и 40 см²", "Отношение 1:2, всего 3 части. 60 ÷ 3 = 20. Части: 20 и 40.", (20, 40), _d2, multi_input=True),
    Task(3, "Уровень 1", "Базовый 3", "Площадь 120 см² разделили в отношении 1:3. Найдите площадь большей части.", "90 см²", "Всего 4 части, 120 ÷ 4 = 30. Большая: 30 × 3 = 90.", (90,), _d3),
    Task(4, "Уровень 1", "Базовый 4", "Одна часть 20 см², вторая в 4 раза больше. Найдите площадь целого прямоугольника.", "100 см²", "Отношение 1:4, всего 5 частей. Если 1 часть = 20, то целое 20 × 5 = 100.", (100,), _d4),
    Task(5, "Уровень 1", "Базовый 5", "Большая часть 120 см² и она в 3 раза больше меньшей. Найдите общую площадь.", "160 см²", "120 = 3 части, 1 часть = 40. Всего 4 части: 40 × 4 = 160.", (160,), _d5),
    Task(6, "Уровень 2", "Средний 6", "Прямоугольник 8×15 см разрезали по короткой стороне в отношении 1:3. Найдите площади фигур (через запятую).", "30 см² и 90 см²", "8 делим на 4: 2 и 6. Площади: 15×2=30 и 15×6=90.", (30, 90), _d6, multi_input=True),
    Task(7, "Уровень 2", "Средний 7", "Прямоугольник 10×20 см разрезали вдоль длинной стороны в отношении 1:4. Найдите площадь меньшей части.", "40 см²", "20 делим на 5, меньшая ширина 4. Площадь: 10×4 = 40.", (40,), _d7),
    Task(
        8,
        "Уровень 2",
        "Средний 8",
        "Площадь 180 см², сторона 10 см. Разрез в отношении 2:3. Найдите площади частей (через запятую).",
        "72 см² и 108 см²",
        "Вторая сторона: 180 ÷ 10 = 18 см. Делим 18 в отношении 2:3: всего 5 частей, одна часть 18 ÷ 5 = 3,6 см. "
        "Отрезки 7,2 см и 10,8 см. Площади: 10×7,2 = 72 и 10×10,8 = 108.",
        (72, 108),
        _d8,
        multi_input=True,
    ),
    Task(
        9,
        "Уровень 2",
        "Средний 9",
        "Квадрат 12×12 см разрезали в отношении 1:3. Введите площади двух фигур (через запятую).",
        "36 см² и 108 см²",
        "Сторону 12 см делим в отношении 1:3: всего 4 части по длине, получаются отрезки 3 см и 9 см. Площади: 12·3 = 36 и 12·9 = 108.",
        (36, 108),
        _d9,
        multi_input=True,
    ),
    Task(
        10,
        "Уровень 2",
        "Средний 10",
        "Площадь прямоугольника 400 см². Одна часть — квадрат 10×10. Во сколько раз вторая часть больше первой?",
        "3 раза",
        "Квадрат 10×10 даёт площадь 100 см². Тогда вторая часть по площади 400 − 100 = 300 см². Сравниваем: 300 ÷ 100 = 3.",
        (3,),
        _d10,
    ),
    Task(
        11,
        "Уровень 3",
        "Сложный 11",
        "Площади частей относятся как 3:5, разница 40 см². Найдите площадь всего прямоугольника.",
        "160 см²",
        "Пусть части 3k и 5k. Разница 5k − 3k = 2k = 40, значит k = 20. Всего 3k + 5k = 8k = 160.",
        (160,),
        _d11,
    ),
    Task(
        12,
        "Уровень 3",
        "Сложный 12",
        "Прямоугольник 300×50 см, одна часть — квадрат 50×50. Найдите площадь второй части.",
        "12500 см²",
        "Вся площадь 300·50 = 15000 см². Квадрат 50·50 = 2500 см². Вторая часть: 15000 − 2500 = 12500.",
        (12500,),
        _d12,
    ),
    Task(
        13,
        "Уровень 3",
        "Сложный 13",
        "Площади частей относятся как 1:6. Большая часть на 100 см² больше меньшей. Найдите общую площадь.",
        "140 см²",
        "Пусть площади меньшей и большей частей k и 6k (см²). Тогда 6k − k = 5k = 100, k = 20. Всего k + 6k = 7k = 140.",
        (140,),
        _d13,
    ),
    Task(
        14,
        "Уровень 3",
        "Сложный 14",
        "Три части: первая в 2 раза больше второй, третья равна сумме первых двух. Общая площадь 240 см². Найдите все части (через запятую).",
        "80 см², 40 см², 120 см²",
        "Пусть вторая x см², тогда первая 2x, третья 2x + x = 3x. Сумма 2x + x + 3x = 6x = 240 см², значит x = 40. Части: 80, 40 и 120 см².",
        (80, 40, 120),
        _d14,
        multi_input=True,
        allow_any_order=False,
    ),
    Task(15, "Уровень 3", "Бонус 15", "Если площадь A увеличить в 5 раз, получится площадь всего прямоугольника. Какую часть от целого составляет B? (можно 0.8 или 80)", "4/5 (80%)", "5A = S = A + B => B = 4A. Тогда B/S = 4/5 = 0.8 = 80%.", (0.8,), _d15, bonus_accept_percent=True),
]

PAGES = {
    "Уровень 1": [t for t in TASKS if t.level == "Уровень 1"],
    "Уровень 2": [t for t in TASKS if t.level == "Уровень 2"],
    "Уровень 3": [t for t in TASKS if t.level == "Уровень 3"],
}


def _parse_numbers(raw: str) -> list[float]:
    clean = raw.strip().replace(";", ",")
    if not clean:
        return []
    chunks = [c.strip() for c in re.split(r"[,\s]+", clean) if c.strip()]
    nums: list[float] = []
    for token in chunks:
        token = token.replace("%", "")
        if "/" in token:
            a, b = token.split("/", 1)
            nums.append(float(a) / float(b))
        else:
            nums.append(float(token.replace(",", ".")))
    return nums


def _is_correct(task: Task, user_values: list[float]) -> bool:
    if not user_values:
        return False
    if task.bonus_accept_percent and len(user_values) == 1:
        v = user_values[0]
        return abs(v - 80) < 1e-6 or abs(v - 0.8) < 1e-6 or abs(v - 4 / 5) < 1e-6
    if len(user_values) != len(task.expected):
        return False
    a = sorted(user_values) if task.allow_any_order else user_values
    b = sorted(task.expected) if task.allow_any_order else list(task.expected)
    return all(abs(x - y) < 1e-6 for x, y in zip(a, b))


def _init_state() -> None:
    if "prop_solved_by_level" not in st.session_state:
        st.session_state["prop_solved_by_level"] = {"Уровень 1": set(), "Уровень 2": set(), "Уровень 3": set()}
    if "prop_idx_by_level" not in st.session_state:
        st.session_state["prop_idx_by_level"] = {"Уровень 1": 0, "Уровень 2": 0, "Уровень 3": 0}
    if "prop_celebrated" not in st.session_state:
        st.session_state["prop_celebrated"] = {"Уровень 1": False, "Уровень 2": False, "Уровень 3": False}
    if "prop_stats" not in st.session_state:
        st.session_state["prop_stats"] = {"attempts": 0, "success": 0}


def render_proporsii_trenajer() -> None:
    _init_state()

    st.markdown(
        """
        <style>
        .stApp { color: #0f172a !important; }
        .big-card {
          border-radius: 16px; padding: 14px 16px; background: rgba(255,255,255,0.82);
          border: 1px solid rgba(15,23,42,0.08); box-shadow: 0 4px 12px rgba(15,23,42,0.05);
          margin-bottom: 12px;
        }
        .task-card {
          border-radius: 12px; padding: 10px 12px; border: 1px solid rgba(15,23,42,0.10);
          background: rgba(255,255,255,0.88); margin-bottom: 8px;
        }
        .task-title { font-size: 1.35rem; font-weight: 700; color: #0f172a; margin-bottom: 6px; }
        .task-text { font-size: 1.02rem; font-weight: 500; color: #1e293b; line-height: 1.5; }
        div[data-testid="stCaptionContainer"] p { color: #334155 !important; font-size: 0.95rem !important; }
        div[data-testid="stMarkdownContainer"] p { color: #0f172a !important; font-size: 1rem !important; }
        label p { color: #0f172a !important; font-size: 1rem !important; font-weight: 500 !important; }
        .level-progress-wrap {
          width: 100%;
          height: 0.55rem;
          border-radius: 999px;
          background: #d1d5db;
          overflow: hidden;
          margin-top: 0.2rem;
        }
        .level-progress-fill {
          height: 100%;
          border-radius: 999px;
          background: linear-gradient(90deg, #16a34a, #22c55e);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("📦🍫✨ Тренажер пропорций и площадей")
    st.caption("5 класс · учимся понимать отношения, площади и логику разрезаний")

    tab_home, tab_trainer, tab_check = st.tabs(["🏠 Главная", "✏️ Тренажер", "✅ Проверка"])

    with tab_home:
        st.markdown(
            """
            <div class="big-card">
              <h3>Шпаргалка: как решать такие задачи</h3>
              <p><b>1)</b> Переводи условие в отношение (например, 1:3).</p>
              <p><b>2)</b> Считай общее число частей (1+3=4).</p>
              <p><b>3)</b> Находи одну часть и умножай.</p>
              <p><b>4)</b> Проверяй: сумма частей = целое.</p>
            </div>
            <div class="big-card">
              <h3>Как пользоваться тренажером</h3>
              <p>Выбери уровень → решай задачи по очереди → нажимай «Проверить».</p>
              <p>Когда по уровню будет 100% верных решений — прилетит конфетти 🎉</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab_trainer:
        level = st.selectbox("Выбери уровень", ["Уровень 1", "Уровень 2", "Уровень 3"], key="prop_level")
        current_tasks = PAGES[level]
        idx = st.session_state["prop_idx_by_level"][level]
        task = current_tasks[idx]

        total = len(current_tasks)
        stats_slot = st.empty()
        progress_slot = st.empty()

        def _render_stats_now() -> None:
            _stats = st.session_state["prop_stats"]
            _att = _stats["attempts"]
            _ok = _stats["success"]
            _pct = (_ok / _att) if _att > 0 else 0.0
            with stats_slot.container():
                st.markdown("##### 📊 Статистика за сеанс")
                _m1, _m2, _m3 = st.columns(3)
                _m1.metric("Всего проверок", _att)
                _m2.metric("Верных ответов", _ok)
                _m3.metric("Доля верных", f"{_pct * 100:.0f}%" if _att else "—")
                if _att > 0:
                    st.progress(_pct, text=f"{_ok} верных из {_att} попыток ({_pct * 100:.0f}%)")
                else:
                    st.caption("Здесь появится полоска прогресса после первой проверки ответа.")

        def _render_progress_now() -> None:
            solved_now = len(st.session_state["prop_solved_by_level"][level])
            with progress_slot.container():
                st.markdown("##### 🎯 Прогресс выбранного уровня")
                pct = solved_now / total if total else 0.0
                st.caption(f"Решено задач: {solved_now} из {total}")
                st.markdown(
                    f"""
                    <div class="level-progress-wrap">
                      <div class="level-progress-fill" style="width:{pct * 100:.1f}%"></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        _render_stats_now()
        _render_progress_now()
        st.markdown("---")

        c_prev, c_next, c_meta = st.columns([1, 1, 2], vertical_alignment="center")
        with c_prev:
            if st.button("⬅️ Предыдущая", use_container_width=True, disabled=idx == 0, key=f"prop_prev_{level}"):
                st.session_state["prop_idx_by_level"][level] = max(0, idx - 1)
                st.rerun()
        with c_next:
            if st.button("Следующая ➡️", use_container_width=True, disabled=idx == total - 1, key=f"prop_next_{level}"):
                st.session_state["prop_idx_by_level"][level] = min(total - 1, idx + 1)
                st.rerun()
        with c_meta:
            st.caption(f"Задача {idx + 1} из {total} в уровне · №{task.number} из 15")

        st.markdown(
            f"""
            <div class="task-card">
              <div class="task-title">{task.title}</div>
              <div style="margin-bottom:0.4rem;color:#0369a1;font-weight:600;">{level}</div>
              <div class="task-text">{task.text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p style="margin:0.1rem 0 0.3rem 0;font-weight:600;color:#0f172a;">Чертёж</p>',
            unsafe_allow_html=True,
        )
        fig, ax = plt.subplots(figsize=(5.4, 2.8), dpi=140)
        task.draw(ax)
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.02, facecolor="white")
        plt.close(fig)
        buf.seek(0)
        st.image(buf, width=520)

        st.markdown(
            '<p style="margin:0.75rem 0 0.35rem 0;font-weight:600;color:#0f172a;">Попробуй решить сам</p>',
            unsafe_allow_html=True,
        )
        if task.multi_input:
            raw = st.text_input(
                "Ответ (числа через запятую)",
                key=f"prop_input_{level}_{task.number}",
                placeholder="например: 20, 40",
            )
            parsed = _parse_numbers(raw) if raw else []
        else:
            val = st.number_input(
                "Ответ (число)",
                key=f"prop_input_{level}_{task.number}",
                value=0.0,
                step=1.0,
                format="%.6g",
            )
            parsed = [float(val)]

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Проверить ответ", type="primary", use_container_width=True, key=f"prop_check_{task.number}_{level}"):
                st.session_state["prop_stats"]["attempts"] += 1
                if _is_correct(task, parsed):
                    st.success("Верно! Отличная работа ✨")
                    st.session_state["prop_solved_by_level"][level].add(task.number)
                    st.session_state["prop_stats"]["success"] += 1
                    st.balloons()
                else:
                    st.error("Пока неверно. Подумай еще и попробуй снова 💡")
                _render_stats_now()
                _render_progress_now()
        with c2:
            if st.button("Показать ответ", use_container_width=True, key=f"prop_show_{task.number}_{level}"):
                st.warning(f"Ответ: {task.answer_text}")
                st.info(task.explanation)

    with tab_check:
        st.subheader("Все решения для самопроверки")
        for lv in ["Уровень 1", "Уровень 2", "Уровень 3"]:
            st.markdown(f"### {lv}")
            for t in PAGES[lv]:
                with st.expander(f"№{t.number}. {t.text}", expanded=False):
                    st.markdown(f"**Ответ:** {t.answer_text}")
                    st.markdown(f"**Объяснение:** {t.explanation}")
