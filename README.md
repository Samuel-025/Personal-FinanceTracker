# 💰 Personal Finance Tracker

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-4ade80?style=flat-square&logo=github)](https://samuel-025.github.io/Personal-FinanceTracker/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

A personal finance tracker with two modes:
- 🌐 **Web Dashboard** — runs fully in the browser with persistent `localStorage` support
- 🖥️ **Python CLI** — terminal app that saves data to a local CSV

---

## 🚀 Live Demo

👉 **[samuel-025.github.io/Personal-FinanceTracker](https://samuel-025.github.io/Personal-FinanceTracker/)**

No login. No install. Just open and start tracking.

---

## ✨ Features

### 🌐 Web Dashboard
- **Dashboard** — KPI cards (income, expenses, net savings, transaction count), Income vs Expenses line chart (3M / 6M / 1Y / All), spending doughnut chart, recent transactions list
- **Add Transaction** — form with date, amount (₹), category (income/expense), description, and validation
- **Transactions** — sortable table, filters by date range / type / category, global search, inline edit & delete, CSV export
- **Analytics** — 12-month bar chart, income & expense breakdowns by category with progress bars
- **Budgets** — set monthly limits per expense category, live progress bars, over-budget alerts
- **Persistent Storage** — saves automatically to browser `localStorage` so data survives page refreshes
- 🌙 Dark / ☀️ Light mode toggle
- 📱 Mobile responsive with collapsible sidebar
- 🇮🇳 Currency formatted in Indian Rupees (₹)

### 🖥️ Python CLI
- Add, view, update, and delete transactions stored in `finance_data.csv`
- Filter transactions by date range
- Plot daily income vs expenses and monthly summaries (Matplotlib)
- Export data to CSV
- Automatic UTF-8 terminal encoding and robust input validation

---

## 🌐 Using the Web Dashboard

### Option 1 — Use the Live Site (Easiest)

Just visit:
```
https://samuel-025.github.io/Personal-FinanceTracker/
```
No installation, no account, works on any device.

> 💾 **Note:** Data is saved automatically to your browser's `localStorage`. You can also export your data anytime to a `.csv` file via the **Transactions** tab.

---

### Option 2 — Run Locally (Offline)

1. **Download or clone the repo:**

```bash
git clone https://github.com/Samuel-025/Personal-FinanceTracker.git
cd Personal-FinanceTracker
```

2. **Open the dashboard:**

Just double-click `index.html` — or open it in any modern browser:

```bash
# macOS
open index.html

# Linux
xdg-open index.html

# Windows (Command Prompt)
start index.html
```

That's it. No server, no dependencies, no build step.

---

## 🖥️ Using the Python CLI

### Requirements
- Python 3.8 or higher
- pip

### Step 1 — Clone the repo

```bash
git clone https://github.com/Samuel-025/Personal-FinanceTracker.git
cd Personal-FinanceTracker
```

### Step 2 — (Recommended) Create a virtual environment

```bash
# Create venv
python -m venv .venv

# Activate it
# Windows (PowerShell):
.\.venv\Scripts\activate

# macOS / Linux:
source .venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run the app

```bash
python main.py
```

### CLI Menu Options

```
1. Add new transaction
2. View transactions
3. Update a transaction
4. Delete a transaction
5. Plot monthly summary
6. Export CSV file
7. Exit
```

Data is saved automatically to `finance_data.csv` in the project folder (created on first run).

---

## 📁 Project Structure

```
Personal-FinanceTracker/
├── main.py             # CLI app — add/view/update/delete/plot
├── data_entry.py       # Input helpers and validators for CLI
├── requirements.txt    # Python dependencies (pandas, matplotlib)
├── index.html          # Full web dashboard (GitHub Pages entry point)
├── pyproject.toml      # Linter & Pyrefly project settings
├── pyrefly.toml        # Type checker search paths
├── LICENSE             # MIT License
└── README.md
```

> `finance_data.csv` is generated locally by the CLI on first run and is excluded from version control (`.gitignore`).

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | Run `pip install -r requirements.txt` |
| `python` not recognized on Windows | Use `python3` or install Python from [python.org](https://www.python.org/) |
| Charts not showing (CLI) | Ensure `matplotlib` is installed: `pip install matplotlib` |
| `index.html` opens as text | Right-click → Open With → your browser |

---

## 🐛 Bug Fixes Log

| File | Bug | Fix |
|---|---|---|
| `data_entry.py` | Typos in error messages (`frmat`, `entr`, `Account`) | Corrected all three |
| `data_entry.py` | Unfriendly raw exception text in `get_amount()` | Cleaned up validation error messages |
| `main.py` | `sort_csv_by_date()` saved datetime objects instead of strings | Added string conversion before saving |
| `main.py` | `update_entry()` used `if new_amount:` — falsy for `0` | Changed to `if new_amount is not None:` |
| `main.py` | `plot_transactions()` used wrong index for `reindex()` | Fixed to use `pd.date_range()` for clean daily index |
| `main.py` | Monthly plot showed net only instead of separate lines | Split into two `resample("ME")` series |
| `main.py` | `FileNotFoundError` / `EmptyDataError` when CSV missing | Added automatic `CSV.initialize_csv()` on startup |
| `main.py` | Entries without description failed delete/update | Used `df['description'].fillna('')` for NaN matching |
| `main.py` | Windows Rupee symbol (`₹`) terminal encoding crash | Configured UTF-8 stdout encoding on startup |
| `main.py` | Pyrefly static type checking warnings | Applied typed `.apply()` date formatters and clean DataFrame exports |
| `index.html` | Seeded with demo transactions on load | Starts clean with empty transactions array |
| `index.html` | Chart canvas destroyed when no data | Added container wrappers (`wrap-doughnut`, `wrap-income`, `wrap-expense`) |
| `index.html` | Web Dashboard data lost on page refresh | Added `localStorage` automatic state persistence |
| `finance_data.csv` | Personal data committed to repo | Deleted from repo, now gitignored |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — free to use, modify, and distribute.
