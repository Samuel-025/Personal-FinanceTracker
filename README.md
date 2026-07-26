# 💰 Personal Finance Tracker V2

[![CI Status](https://github.com/Samuel-025/Personal-FinanceTracker/actions/workflows/ci.yml/badge.svg)](https://github.com/Samuel-025/Personal-FinanceTracker/actions)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-4ade80?style=flat-square&logo=github)](https://samuel-025.github.io/Personal-FinanceTracker/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

> **Repository Description**: 💰 Unified Personal Finance Tracker featuring a FastAPI + SQLite backend REST API, Rich Terminal CLI, multi-currency Web Dashboard, and PDF/Excel report exports.

A unified personal finance management suite featuring:
- ⚡ **FastAPI + SQLite Backend (`server.py`)** — REST API with automatic Swagger docs (`/docs`), auto-migrating legacy `finance_data.csv` on startup.
- 🎨 **Rich Terminal CLI (`main.py`)** — Beautiful colored console UI with KPI panels, category manager, budget goals, recurring rules, and visual charts.
- 🌐 **Enhanced Web Dashboard (`index.html`)** — Dual Sync Mode (API auto-detect with `localStorage` offline fallback), multi-currency switcher (INR ₹, USD $, EUR €), PDF & Excel exports.

---

### 🏷️ GitHub Repository Topics Set
Copy & paste these topics into the GitHub Repository **About ⚙️** settings:

```text
personal-finance, finance-tracker, fastapi, sqlite, rich-cli, pdf-export, excel-export, budget-manager, multi-currency, chartjs, dashboard, python3
```

---

## 🚀 Quick Start

### Step 1 — Clone & Set Up Environment

```bash
git clone https://github.com/Samuel-025/Personal-FinanceTracker.git
cd Personal-FinanceTracker

# Create & activate virtual environment
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 2 — Run the Unified FastAPI Backend

```bash
python -m uvicorn server:app --reload --port 8000
```
- 🌐 **Web Dashboard**: `http://localhost:8000/`
- 📚 **Interactive Swagger API Docs**: `http://localhost:8000/docs`

---

### Step 3 — Run the Rich Interactive Terminal CLI

In a new terminal window (with `.venv` activated):

```bash
python main.py
```

---

## ✨ Features

### ⚡ Unified Backend & Storage
- **SQLAlchemy + SQLite (`finance.db`)**: Persistent relational storage shared across CLI and Web Dashboard.
- **Auto-Migration**: Automatically parses legacy `finance_data.csv` on first boot and populates SQLite.
- **RESTful Endpoints**: Full CRUD for transactions, categories, budget goals, and recurring rules.

### 🎨 Rich Python CLI
- **Rich Terminal Styling**: Colored tables, KPI summary cards, and interactive prompts.
- **Category Manager**: Add custom categories with emoji icons and custom colors.
- **Budget Goals**: Set category monthly spending limits with live progress bars.
- **Recurring Transactions**: Define auto-posting weekly/monthly income and bills.
- **Multi-Format Reports**: Export PDF summary reports (`.pdf`), Excel spreadsheets (`.xlsx`), or CSV (`.csv`).

### 🌐 Web Dashboard
- **Dual Mode Sync**: Auto-detects FastAPI server at `http://localhost:8000/api` with seamless fallback to browser `localStorage` when offline.
- **Multi-Currency Support**: Switch live between **INR (₹)**, **USD ($)**, and **EUR (€)**.
- **Charts & Insights**: Interactive Line, Doughnut, and Bar charts powered by Chart.js.
- **Export Buttons**: Generate PDF balance sheets and Excel spreadsheets directly from the dashboard.

---

## 📁 Project Structure

```
Personal-FinanceTracker/
├── server.py           # FastAPI REST API server & report generators
├── models.py           # SQLAlchemy ORM database models
├── database.py         # SQLite engine setup & CSV auto-migrator
├── main.py             # Rich-powered interactive Python CLI
├── data_entry.py       # Input helpers & validation handlers
├── index.html          # Web Dashboard UI (Dual Sync Mode)
├── requirements.txt    # Python dependencies (FastAPI, Rich, ReportLab, OpenPyXL)
├── pyproject.toml      # Project & linter settings
├── pyrefly.toml        # Type checker configuration
├── LICENSE             # MIT License
└── README.md
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'fastapi'` | Ensure `.venv` is activated and run `pip install -r requirements.txt` |
| Port 8000 in use | Run server on another port: `uvicorn server:app --port 8080` |
| Web Dashboard displays "Offline Mode" | Ensure `python -m uvicorn server:app` is running on port 8000 |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — free to use, modify, and distribute.
