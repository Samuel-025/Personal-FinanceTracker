# 💰 Personal Finance Tracker V2

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-4ade80?style=flat-square&logo=github)](https://samuel-025.github.io/Personal-FinanceTracker/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

A complete personal finance management system offering three operating modes:
- 🌐 **Web Dashboard** — modern single-page dashboard with automatic live REST API synchronization and offline `localStorage` fallback
- ⚡ **FastAPI REST Server** — SQLite backend providing CRUD endpoints, recurring rule automation, and PDF/Excel/CSV report generation
- 🖥️ **Python CLI** — interactive terminal application for local CSV budget tracking

---

## 🚀 Quick Start

### 1. Live Web Demo (Standalone / Offline Mode)

👉 **[samuel-025.github.io/Personal-FinanceTracker](https://samuel-025.github.io/Personal-FinanceTracker/)**

No installation or account required. Data persists locally in your browser's `localStorage`.

---

### 2. Full Stack Setup (FastAPI Backend + Web Dashboard)

Run the full application locally with SQLite database persistence:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Samuel-025/Personal-FinanceTracker.git
   cd Personal-FinanceTracker
   ```

2. **Set up a Python virtual environment:**
   ```bash
   python -m venv .venv

   # Windows (PowerShell):
   .\.venv\Scripts\activate

   # macOS / Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the FastAPI server:**
   ```bash
   uvicorn server:app --reload --port 8000
   ```

5. **Access the Web Dashboard:**
   Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.
   The top bar will display **`🟢 API Connected (SQLite)`** indicating live database sync.

---

### 3. Terminal CLI Application

Run the interactive Python terminal app:

```bash
python main.py
```

CLI Data is stored in `finance_data.csv` (automatically migrated to SQLite when starting the backend server).

---

## ✨ Features

### 🌐 Web Dashboard (`index.html`)
- **Live Server Auto-Detection** — auto-detects `http://127.0.0.1:8000/` server connection; falls back seamlessly to browser `localStorage` when offline.
- **KPI Metrics** — real-time cards for monthly income, expenses, net savings surplus/deficit, and transaction counts.
- **Visual Analytics** — interactive 12-month bar charts, expense breakdown doughnuts, and progress summaries using Chart.js.
- **Multi-Select & Batch Delete** — table header select-all checkbox and row selection to batch delete transactions via REST API.
- **Transaction Filters & Export** — filter by date range, type (Income/Expense), or category, global search, inline editing, and CSV exports.
- **Budget Tracking** — monthly spending limits per category with live progress bars and over-budget warnings.
- **Categories** — full support for Income (Salary, Freelance, Investment, Business, Other) and Expense (Food, Groceries 🛒, Transport, Housing, Utilities, Healthcare, Entertainment, Shopping, Education, Travel, Other) categories.
- **Dark / Light Theme** — toggleable UI theme with persistent setting.
- **Localization** — Indian Rupee (`₹`) currency formatting and `dd-mm-yyyy` date display.

### ⚡ FastAPI REST API (`server.py`)
- **SQLite Database Integration** — SQLAlchemy 2.0 ORM models (`Transaction`, `Category`, `Budget`, `RecurringRule`).
- **CSV Auto-Migration** — automatically imports `finance_data.csv` records into SQLite (`finance.db`) on initial startup with format normalization.
- **Referential Integrity** — category deletion endpoint checks for active references in transactions, budgets, or recurring rules (returns HTTP 409 Conflict if in use).
- **Recurring Automation** — processes due recurring income/expense rules with calendar month-length date-drift preservation.
- **Document Export Endpoints**:
  - `GET /api/export/pdf` — generates formatted PDF summary report using ReportLab.
  - `GET /api/export/excel` — generates styled Excel workbook with cell formatting using openpyxl.
  - `GET /api/export/csv` — generates raw CSV file export.

### 🖥️ Python CLI (`main.py`)
- Interactive menu to add, view, update, and delete transactions.
- Filter transactions by custom date ranges.
- Render Matplotlib charts for monthly income vs expense trends.
- UTF-8 terminal encoding and input validation.

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the Web Dashboard SPA (`index.html`) |
| `GET` | `/api/transactions` | List all transactions (supports `start_date`, `end_date`, `category`, `type` query filters) |
| `POST` | `/api/transactions` | Create a new transaction |
| `PUT` | `/api/transactions/{id}` | Update an existing transaction |
| `DELETE` | `/api/transactions/{id}` | Delete a transaction by ID |
| `GET` | `/api/categories` | List all categories |
| `POST` | `/api/categories` | Create a new custom category |
| `DELETE` | `/api/categories/{id}` | Delete a category (returns HTTP 409 if category is in active use) |
| `GET` | `/api/budgets` | List all category budgets |
| `POST` | `/api/budgets` | Create or update a monthly category budget limit |
| `DELETE` | `/api/budgets/{category_name}` | Delete a budget limit |
| `GET` | `/api/recurring` | List all recurring transaction rules |
| `POST` | `/api/recurring` | Create a new recurring rule |
| `POST` | `/api/recurring/process` | Process active recurring rules and generate due transactions |
| `GET` | `/api/export/pdf` | Generate and download PDF report |
| `GET` | `/api/export/excel` | Generate and download Excel workbook report |
| `GET` | `/api/export/csv` | Download CSV export |

---

## 📁 Project Structure

```
Personal-FinanceTracker/
├── server.py           # FastAPI REST API server & PDF/Excel/CSV exports
├── database.py         # SQLAlchemy engine, SQLite setup & CSV auto-migration
├── models.py           # SQLAlchemy 2.0 Mapped ORM models (Transaction, Category, Budget, RecurringRule)
├── main.py             # Interactive Python CLI application
├── data_entry.py       # Input helper functions and validators for CLI
├── index.html          # Single-Page Web Dashboard (live API auto-sync & localStorage mode)
├── requirements.txt    # Python dependencies (FastAPI, SQLAlchemy, Pandas, Matplotlib, ReportLab, etc.)
├── pyproject.toml      # Linter and project configurations
├── pyrefly.toml        # Type checker search paths
├── LICENSE             # MIT License
├── CONTRIBUTING.md     # Guidelines for contributors
└── README.md           # Project documentation
```

---

## 🛠️ Troubleshooting

| Issue | Solution |
|---|---|
| Dashboard shows `🔴 Offline (localStorage)` | Start the FastAPI server using `uvicorn server:app --reload --port 8000` |
| `ModuleNotFoundError` on startup | Run `pip install -r requirements.txt` inside your virtual environment |
| `python` command not found on Windows | Use `python3` or add Python to system `PATH` |
| Category deletion fails (409 Conflict) | Remove or update transactions/budgets/recurring rules referencing the category first |
| `index.html` opens as plain text | Double click `index.html` or use Right Click → Open With → Browser |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — free to use, modify, and distribute.
