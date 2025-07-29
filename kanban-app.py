# kanban_app.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
from fpdf import FPDF
import plotly.express as px
import json
import os
from datetime import datetime

# === Firebase Setup ===
import os
service_account_info = st.secrets["firebase_service_account"]
cred = credentials.Certificate(service_account_info)


if not firebase_admin._apps:
    service_account_info = json.loads(st.secrets["firebase_service_account"])
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://kanban-teams-default-rtdb.firebaseio.com/'
    })

# === Language Setup ===
LANGUAGES = {
    "English": {
        "login": "Login",
        "create_team": "Create New Team",
        "team_name": "Team Name",
        "password": "Password",
        "your_name": "Your Name",
        "add_task": "Add Task",
        "title": "Title",
        "description": "Description",
        "priority": "Priority",
        "due_date": "Due Date",
        "assignee": "Assignee",
        "estimated_time": "Estimated Time (hrs)",
        "column": "Column",
        "add": "Add Task",
        "kanban_board": "Kanban Board",
        "comment": "Comment",
        "add_comment": "Add Comment",
        "dashboard": "Dashboard",
        "total_tasks": "Total Tasks",
        "total_hours": "Total Hours",
        "download_pdf": "Download PDF",
        "download_excel": "Download Excel",
        "login_or_create": "Login or Create Team"
    },
    "Русский": {
        "login": "Войти",
        "create_team": "Создать команду",
        "team_name": "Название команды",
        "password": "Пароль",
        "your_name": "Ваше имя",
        "add_task": "Добавить задачу",
        "title": "Заголовок",
        "description": "Описание",
        "priority": "Приоритет",
        "due_date": "Срок",
        "assignee": "Исполнитель",
        "estimated_time": "Оценочное время (часы)",
        "column": "Колонка",
        "add": "Добавить задачу",
        "kanban_board": "Канбан доска",
        "comment": "Комментарий",
        "add_comment": "Добавить комментарий",
        "dashboard": "Дашборд",
        "total_tasks": "Всего задач",
        "total_hours": "Всего часов",
        "download_pdf": "Скачать PDF",
        "download_excel": "Скачать Excel",
        "login_or_create": "Войти или создать команду"
    },
    "Azərbaycan": {
        "login": "Daxil ol",
        "create_team": "Yeni komanda yarat",
        "team_name": "Komanda adı",
        "password": "Şifrə",
        "your_name": "Adınız",
        "add_task": "Tapşırıq əlavə et",
        "title": "Başlıq",
        "description": "Təsvir",
        "priority": "Üstünlük",
        "due_date": "Son tarix",
        "assignee": "Təyin edilən",
        "estimated_time": "Təxmini vaxt (saat)",
        "column": "Sütun",
        "add": "Tapşırıq əlavə et",
        "kanban_board": "Kanban lövhəsi",
        "comment": "Şərh",
        "add_comment": "Şərh əlavə et",
        "dashboard": "Panel",
        "total_tasks": "Ümumi tapşırıqlar",
        "total_hours": "Ümumi saat",
        "download_pdf": "PDF yüklə",
        "download_excel": "Excel yüklə",
        "login_or_create": "Daxil ol və ya komanda yarat"
    }
}

# === Constants ===
COLUMNS = {
    "to do": "To Do",
    "in progress": "In Progress",
    "done": "Done"
}
PRIORITIES = ["Low", "Medium", "High"]

# === App Language ===
st.sidebar.header("🌐 Language")
lang_choice = st.sidebar.radio("Choose language", list(LANGUAGES.keys()))
T = LANGUAGES[lang_choice]

# === Firebase Methods ===
def get_team_data():
    return db.reference("/teams").get() or {}

def save_team_data(team_data):
    db.reference("/teams").set(team_data)

def get_user_team(team_name):
    return db.reference(f"/teams/{team_name}").get()

def save_user_team(team_name, data):
    db.reference(f"/teams/{team_name}").set(data)

def export_to_pdf(team_name, task_df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Team Kanban Summary - {team_name}", ln=True, align="C")
    for index, row in task_df.iterrows():
        pdf.multi_cell(0, 10, txt=f"{row.to_string(index=True)}\n")
    filename = f"{team_name}_summary.pdf"
    pdf.output(filename)
    return filename

# === App ===
st.set_page_config(page_title="Kanban App", layout="wide")
st.image("nijat_logo.png", width=100)
st.title("📌 " + T["kanban_board"])

st.sidebar.header("🔐 " + T["login_or_create"])
team_name = st.sidebar.text_input(T["team_name"])
password = st.sidebar.text_input(T["password"], type="password")
user_name = st.sidebar.text_input(T["your_name"])
auth = False

if st.sidebar.button(T["login"]):
    data = get_user_team(team_name)
    if data and data.get("password") == password:
        st.session_state["team"] = team_name
        st.session_state["user"] = user_name
        st.success("Logged in successfully.")
        auth = True
    else:
        st.error("Invalid credentials.")

if "team" in st.session_state:
    team_name = st.session_state.get("team")
    user = st.session_state.get("user")
    team_data = get_user_team(team_name) or {}

    board = team_data.get("board")
    if not board or not isinstance(board, dict):
        board = {key: [] for key in COLUMNS}

    normalized_board = {str(k).strip().lower(): v if isinstance(v, list) else [] for k, v in board.items()}
    for key in COLUMNS:
        if key not in normalized_board:
            normalized_board[key] = []

    team_data["board"] = normalized_board
    save_user_team(team_name, team_data)

    is_lead = team_data.get("lead") == user

    st.subheader("📋 " + T["add_task"])
    with st.form("task_form"):
        title = st.text_input(T["title"])
        desc = st.text_area(T["description"])
        priority = st.selectbox(T["priority"], PRIORITIES)
        due_date = st.date_input(T["due_date"])
        assignee = st.text_input(T["assignee"], value=user)
        time_required = st.number_input(T["estimated_time"], min_value=0.0)
        col_label = st.selectbox(T["column"], list(COLUMNS.values()))
        col = [k for k, v in COLUMNS.items() if v == col_label][0]
        submitted = st.form_submit_button(T["add"])
        if submitted and title:
            new_task = {
                "title": title,
                "desc": desc,
                "priority": priority,
                "due_date": due_date.strftime("%Y-%m-%d"),
                "assignee": assignee,
                "created_by": user,
                "created_at": datetime.now().isoformat(),
                "time_required": time_required,
                "comments": []
            }
            if col not in normalized_board:
                normalized_board[col] = []
            normalized_board[col].append(new_task)
            team_data["board"] = normalized_board
            save_user_team(team_name, team_data)
            st.success("Task added.")

    st.subheader("📌 " + T["kanban_board"])
    cols = st.columns(len(COLUMNS))
    for i, (col_key, col_label) in enumerate(COLUMNS.items()):
        with cols[i]:
            st.markdown(f"### {col_label}")
            for idx, task in enumerate(normalized_board.get(col_key, [])):
                st.markdown(f"**{task['title']}**")
                st.markdown(f"{task['desc']}")
                st.markdown(f"👤 {task['assignee']} | ⏱ {task['time_required']} hrs | 🔥 {task['priority']} | 📅 {task['due_date']}")
                if is_lead:
                    comment = st.text_input(f"💬 {T['comment']} - {task['title']}", key=f"comment_{col_key}_{idx}")
                    if st.button(f"{T['add_comment']} - {task['title']}", key=f"btn_comment_{col_key}_{idx}"):
                        task['comments'].append(comment)
                        save_user_team(team_name, team_data)
                        st.success("Comment added.")

    if is_lead:
        st.subheader("📊 " + T["dashboard"])
        all_tasks = [task | {"status": COLUMNS.get(key, key.title())} for key in normalized_board for task in normalized_board.get(key, [])]
        df = pd.DataFrame(all_tasks)
        if not df.empty:
            st.markdown(f"**{T['total_tasks']}:** {len(df)}")
            st.markdown(f"**{T['total_hours']}:** {df['time_required'].sum()} hrs")
            fig1 = px.pie(df, names="status", title="Tasks by Status")
            st.plotly_chart(fig1)
            fig2 = px.bar(df, x="assignee", color="priority", title="Tasks by Assignee and Priority")
            st.plotly_chart(fig2)
            pdf_file = export_to_pdf(team_name, df)
            with open(pdf_file, "rb") as f:
                st.download_button("📄 " + T["download_pdf"], f, file_name=pdf_file)
            excel_file = f"{team_name}_tasks.xlsx"
            df.to_excel(excel_file, index=False)
            with open(excel_file, "rb") as f:
                st.download_button("📊 " + T["download_excel"], f, file_name=excel_file)
