# 📌 Kanban Teams App (Streamlit + Firebase)

This is a **multi-user Kanban board app** built with **Python + Streamlit** and backed by **Firebase Realtime Database**. It supports **team-based logins**, **task management**, **comments**, **time tracking**, **dashboard visualization**, and **multilingual UI** (English, Russian, Azerbaijani).

---

## 🚀 Features

* 🔐 Team-based login and creation (Team Lead & Members)
* 📋 Add tasks with title, description, priority, due date, assignee, time estimate
* 📌 Kanban board view (To Do / In Progress / Done)
* 💬 Commenting (team leads only)
* 📊 Dashboard: Pie chart, Bar chart, Task summary
* 🌐 Multi-language support (🇬🇧 English, 🇷🇺 Русский, 🇦🇿 Azərbaycan)
* 📤 Export to PDF and Excel

---

## 🛠️ Tech Stack

* **Python 3.10+**
* [Streamlit](https://streamlit.io/) for UI
* [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup) for backend
* **Plotly** for data visualization
* **FPDF** & **Pandas** for export

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/kanban-teams.git
cd kanban-teams
```

### 2. Add Firebase credentials

Place your `serviceAccountKey.json` file in the root folder. You can get this from your Firebase project > Project Settings > Service accounts.

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run kanban-app.py
```

---

## 🔐 Firebase Setup

1. Create a Firebase project
2. Go to "Realtime Database" and create a new database in test mode
3. Go to "Project Settings" > "Service Accounts"
4. Generate new private key — this downloads `serviceAccountKey.json`
5. Set database URL in the script to match your Firebase URL

---

## 🌍 Deployment (Recommended)

Use [Streamlit Cloud](https://streamlit.io/cloud):

1. Push this code to GitHub
2. Go to Streamlit Cloud, sign in, and create a new app from your repo
3. Upload `serviceAccountKey.json` as a **secret**

---

## 📱 Turn Into Android App

Use **Android WebView** to wrap the deployed app. Let us know if you'd like help with this step.

---

## 📁 Files

* `kanban-app.py` — main application script
* `requirements.txt` — required Python packages
* `nijat_logo.png` — your app branding logo
* `serviceAccountKey.json` — Firebase admin key (not shared publicly)

---

## 📬 Questions or Support?

Contact the developer at \[[your.email@example.com](mailto:your.email@example.com)] or open an issue on GitHub.

---

## ✅ License

MIT License
