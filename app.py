import html
import io
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt

from problems_catalog import problems
from proporsii_trenajer_module import render_proporsii_trenajer

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
    .stApp {
        background: #f1f7f2 !important;
    }
    div[data-testid="stImage"],
    div[data-testid="stImage"] > div {
        min-height: 0 !important;
        margin-top: -0.9rem !important;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        align-self: flex-start !important;
    }
    /* Поле ответа: не на всю ширину экрана */
    div[data-testid="stNumberInput"] {
        max-width: 14rem !important;
    }
    div[data-testid="stNumberInput"] label p {
        color: #0f172a !important;
        font-weight: 500 !important;
    }
    /* Полоска st.progress — синяя (в теме заливка = secondary, часто красная) */
    div[data-testid="stProgress"] [role="progressbar"] > div > div > div {
        background-color: #2563eb !important;
        background-image: none !important;
    }
    .start-welcome {
        border-radius: 16px;
        padding: 14px 16px;
        background: linear-gradient(135deg, #dbeafe 0%, #dcfce7 100%);
        border: 1px solid rgba(15, 23, 42, 0.08);
        margin: 0.4rem 0 1rem 0;
    }
    .home-title {
        text-align: center;
        margin: 0.2rem 0 0.35rem 0;
        font-size: 2.6rem;
        line-height: 1.15;
        font-weight: 900;
        color: #0b2b63;
        text-shadow: 0 2px 0 rgba(255, 255, 255, 0.75);
    }
    .home-subtitle {
        text-align: center;
        margin: 0 0 0.8rem 0;
        color: #334155;
        font-size: 1.06rem;
    }
    .start-card {
        border-radius: 14px;
        padding: 14px;
        background: #ffffff;
        border: 1px solid rgba(15, 23, 42, 0.08);
        min-height: 170px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
    }
    .start-card h4 {
        margin: 0 0 0.35rem 0;
        color: #0f172a;
        font-size: 1.1rem;
    }
    .start-card p {
        margin: 0;
        color: #334155;
        line-height: 1.45;
    }
    .dir-btn {
        display: block;
        text-align: center;
        margin-top: 10px;
        padding: 0.52rem 0.8rem;
        border-radius: 0.55rem;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.95rem;
        color: #fff !important;
    }
    .dir-blue { background: #2563eb; border: 1px solid #1d4ed8; }
    .dir-red { background: #ef4444; border: 1px solid #dc2626; }
    .dir-green { background: #22c55e; border: 1px solid #16a34a; }
    </style>
    """,
    unsafe_allow_html=True,
)


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

ARCHIVE_DIR = Path("archive_pdfs")


def _format_size(num_bytes: int) -> str:
    mb = num_bytes / (1024 * 1024)
    if mb >= 1:
        return f"{mb:.2f} MB"
    kb = num_bytes / 1024
    return f"{kb:.0f} KB"


def _collect_theme_pdfs(base_dir: Path) -> dict[str, dict[str, list[Path]]]:
    """
    Ищет PDF в archive_pdfs и группирует по темам и подтемам.
    Пример:
    archive_pdfs/5класс/геометрия/...
    archive_pdfs/5класс/дроби/...
    """
    grouped: dict[str, dict[str, list[Path]]] = {}
    if not base_dir.exists():
        return grouped

    for pdf_path in base_dir.rglob("*.pdf"):
        rel = pdf_path.relative_to(base_dir)
        if len(rel.parts) == 1:
            theme = "Общее"
            subtheme = "Общее"
        else:
            theme = rel.parts[0]
            subtheme = "/".join(rel.parts[1:-1]) if len(rel.parts) > 2 else "Общее"
        grouped.setdefault(theme, {}).setdefault(subtheme, []).append(pdf_path)

    for theme in grouped:
        for subtheme in grouped[theme]:
            grouped[theme][subtheme] = sorted(grouped[theme][subtheme], key=lambda p: p.name.lower())
        grouped[theme] = dict(sorted(grouped[theme].items(), key=lambda item: item[0].lower()))
    return dict(sorted(grouped.items(), key=lambda item: item[0].lower()))


def _render_library() -> None:
    st.subheader("📚 Библиотека материалов")
    st.caption("Здесь хранятся полезные PDF-материалы по темам и подтемам.")

    theme_pdfs = _collect_theme_pdfs(ARCHIVE_DIR)
    if not theme_pdfs:
        st.info("Библиотека пока пуста. Добавьте PDF-файлы в папку `archive_pdfs` по темам и подтемам.")
        st.markdown(
            """
            **Пример структуры:**
            - `archive_pdfs/5класс/геометрия/урок_1.pdf`
            - `archive_pdfs/5класс/дроби/тренажер.pdf`
            - `archive_pdfs/контрольные/вариант1/контрольная.pdf`
            """
        )
        return

    c_theme, c_subtheme = st.columns(2)
    with c_theme:
        theme_names = list(theme_pdfs.keys())
        theme_counts = {theme: sum(len(files) for files in subthemes.values()) for theme, subthemes in theme_pdfs.items()}
        current_theme = st.selectbox(
            "Тема",
            theme_names,
            index=0,
            format_func=lambda t: f"{t} ({theme_counts[t]})",
        )
    with c_subtheme:
        subtheme_names = list(theme_pdfs[current_theme].keys())
        subtheme_counts = {sub: len(files) for sub, files in theme_pdfs[current_theme].items()}
        current_subtheme = st.selectbox(
            "Подтема",
            subtheme_names,
            index=0,
            format_func=lambda s: f"{s} ({subtheme_counts[s]})",
        )
    st.caption(f"Файлов в выбранной подтеме: {len(theme_pdfs[current_theme][current_subtheme])}")

    for pdf_path in theme_pdfs[current_theme][current_subtheme]:
        file_size = _format_size(pdf_path.stat().st_size)
        rel_path = pdf_path.relative_to(ARCHIVE_DIR).as_posix()
        c_name, c_size, c_dl = st.columns([5, 2, 2], vertical_alignment="center")
        with c_name:
            st.markdown(f"📄 **{pdf_path.name}**")
            st.caption(f"`{rel_path}`")
        with c_size:
            st.caption(file_size)
        with c_dl:
            st.download_button(
                "Скачать",
                data=pdf_path.read_bytes(),
                file_name=pdf_path.name,
                mime="application/pdf",
                key=f"download_{rel_path}",
                use_container_width=True,
            )



# ---------- UI ----------

st.markdown('<h1 class="home-title">🎒 Учебные тренажеры</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="home-subtitle">Выбери тему занятия: геометрия квартиры, пропорции и площади, '
    "и в будущем — новые разделы.</p>",
    unsafe_allow_html=True,
)

if "selected_module" not in st.session_state:
    st.session_state["selected_module"] = "home"

query_module = st.query_params.get("module")
if query_module in {"home", "geometry", "proportions", "library", "soon"}:
    st.session_state["selected_module"] = str(query_module)

top_l, top_r = st.columns([8, 1], vertical_alignment="top")
with top_l:
    if st.session_state["selected_module"] != "home":
        if st.button("🏠 На стартовую", key="go_home"):
            st.session_state["selected_module"] = "home"
            st.query_params["module"] = "home"
            st.rerun()
with top_r:
    if st.button("📚 Библиотека", key="open_library_corner", use_container_width=True):
        st.session_state["selected_module"] = "library"
        st.query_params["module"] = "library"
        st.rerun()

if st.session_state["selected_module"] == "home":
    st.markdown(
        """
        <div class="start-welcome">
          <h3 style="margin:0 0 0.4rem 0;">Привет! 👋 Выбери, чем хочешь заняться сегодня</h3>
          <p style="margin:0;color:#334155;">
            Нажми на карточку направления: можно решать задачи по квартире, тренироваться с пропорциями
            или заглянуть в будущие темы.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Твои данные")
    st.caption("Заполни один раз — имя и класс будут использоваться в тренажерах.")
    home_name_col, home_grade_col = st.columns([4, 1], gap="small")
    with home_name_col:
        home_name = st.text_input(
            "Как тебя зовут?",
            value=st.session_state["name"],
            placeholder="Например, Маша",
            max_chars=40,
            key="home_name",
        )
    with home_grade_col:
        home_grade = st.text_input(
            "Класс",
            value=st.session_state["grade"],
            placeholder="5А",
            max_chars=8,
            key="home_grade",
        )

    st.session_state["name"] = home_name or ""
    st.session_state["grade"] = home_grade or ""
    st.markdown("---")

    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        st.markdown(
            """
            <div class="start-card">
              <h4>📐 Геометрия квартиры</h4>
              <p>Планы комнат, коридоры, площади и задачи по уровням сложности.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<a class="dir-btn dir-blue" href="?module=geometry">Открыть направление</a>', unsafe_allow_html=True)
    with c2:
        st.markdown(
            """
            <div class="start-card">
              <h4>🍫 Тренажер пропорций и площадей</h4>
              <p>Интерактивные задачи 1-3 уровня, проверка ответов и пошаговые объяснения.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<a class="dir-btn dir-red" href="?module=proportions">Открыть направление</a>', unsafe_allow_html=True)
    with c3:
        st.markdown(
            """
            <div class="start-card">
              <h4>✨ Скоро новые темы</h4>
              <p>Здесь будут появляться новые тренажеры по другим разделам математики.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<a class="dir-btn dir-green" href="?module=soon">Открыть направление</a>', unsafe_allow_html=True)

    st.stop()

if st.session_state["selected_module"] == "proportions":
    render_proporsii_trenajer()
    st.stop()

if st.session_state["selected_module"] == "library":
    _render_library()
    st.stop()

if st.session_state["selected_module"] == "soon":
    st.subheader("✨ Скоро новые темы")
    st.info(
        "Здесь будут появляться новые тренажеры по другим разделам математики. "
        "Сейчас доступны направления: «Геометрия квартиры» и «Тренажер пропорций и площадей»."
    )
    st.stop()

st.title("📐 Геометрия квартиры")
st.caption("Задачи для 5 класса · план квартиры, площади, коридоры")

tab_theory, tab_practice = st.tabs(["📖 Правила", "✏️ Задачи"])

with tab_theory:
    st.subheader("Наши инструменты")
    cols = st.columns(len(theory_cards))
    for col, (icon, title, desc) in zip(cols, theory_cards):
        with col:
            st.markdown(f"### {icon} {title}")
            st.write(desc)

with tab_practice:
    if st.session_state["name"] and st.session_state["grade"]:
        st.markdown(f"👋 Привет, **{st.session_state['name']}**! Класс **{st.session_state['grade']}** — удачи!")
    elif st.session_state["name"]:
        st.markdown(f"👋 Привет, **{st.session_state['name']}**!")
    elif st.session_state["grade"]:
        st.markdown(f"Класс **{st.session_state['grade']}**.")

    # Слот заполняется в конце вкладки — после нажатия «Проверить», чтобы числа обновлялись сразу
    stats_slot = st.empty()

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

            _t = html.escape(problem.title)
            _lv = html.escape(problem.lvl)
            st.markdown(
                f'<h3 style="margin:0 0 0.35rem 0;color:#0f172a;font-size:1.35rem;">{_t}</h3>'
                f'<p style="margin:0 0 0.65rem 0;color:#334155;font-size:1rem;font-weight:500;">'
                f"Уровень: <span style='color:#0369a1;'>{_lv}</span></p>",
                unsafe_allow_html=True,
            )

            st.markdown(
                '<p style="margin:0 0 0.2rem 0;font-weight:600;color:#0f172a;">Чертёж</p>',
                unsafe_allow_html=True,
            )
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

            st.markdown(
                '<p style="margin:1rem 0 0.4rem 0;font-weight:600;font-size:1.05rem;color:#0f172a;">Условие</p>',
                unsafe_allow_html=True,
            )
            _cond = html.escape(problem.text).replace("\n", "<br/>")
            st.markdown(
                f'<div style="color:#1e293b;line-height:1.55;font-size:1.02rem;">{_cond}</div>',
                unsafe_allow_html=True,
            )

            can_check_numeric = problem.answer_value != 0.0

            if can_check_numeric:
                st.markdown(
                    '<p style="margin:1rem 0 0.4rem 0;font-weight:600;font-size:1.05rem;color:#0f172a;">'
                    "Попробуй решить сам</p>",
                    unsafe_allow_html=True,
                )
                user_value = st.number_input(
                    problem.answer_label,
                    value=0.0,
                    step=1.0,
                    format="%.1f",
                    key=f"answer_{problem.id}",
                )
                check = st.button("Проверить ответ", key=f"check_{problem.id}", type="primary")
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
                st.markdown(
                    '<p style="margin:0.75rem 0 0.4rem 0;font-weight:600;font-size:1.05rem;color:#0f172a;">'
                    "Пошаговое решение</p>",
                    unsafe_allow_html=True,
                )
                for i, step in enumerate(problem.steps, start=1):
                    st.markdown(f"**{i}.** {step}")
                st.markdown(f"**Ответ:** {problem.answer_text}")

    _stats = st.session_state["stats"]
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
            st.progress(
                _pct,
                text=f"{_ok} верных из {_att} попыток ({_pct * 100:.0f}%)",
            )
        else:
            st.caption("Здесь появится полоска прогресса после первой проверки ответа.")

