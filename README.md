# 💰 Personal Finance Tracker

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-4ade80?style=flat-square&logo=github)](https://samuel-025.github.io/Personal-FinanceTracker/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

A personal finance tracker with two modes:
- 🌐 **Web Dashboard** — runs fully in the browser, no install needed
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
- 🌙 Dark / ☀️ Light mode toggle
- 📱 Mobile responsive with collapsible sidebar
- 🇮🇳 Currency formatted in Indian Rupees (₹)

### 🖥️ Python CLI
- Add, view, update, and delete transactions stored in `finance_data.csv`
- Filter transactions by date range
- Plot daily income vs expenses and monthly summaries (Matplotlib)
- Export data to CSV

---

## 🌐 Using the Web Dashboard

### Option 1 — Use the Live Site (Easiest)

Just visit:
```
https://samuel-025.github.io/Personal-FinanceTracker/
```
No installation, no account, works on any device.

> ⚠️ **Note:** Data is stored in memory only — it resets when you close or refresh the tab. For persistent storage, use the CLI.

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
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
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
5. Plot charts
6. Export to CSV
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
| Web dashboard data lost on refresh | Expected — browser storage is in-memory. Use CLI for persistence. |
| `index.html` opens as text | Right-click → Open With → your browser |

---

## 🐛 Bug Fixes Log

| File | Bug | Fix |
|---|---|---|
| `data_entry.py` | Typos in error messages (`frmat`, `entr`, `Account`) | Corrected all three |
| `main.py` | `sort_csv_by_date()` saved datetime objects instead of strings, corrupting CSV on re-read | Added `.dt.strftime()` before saving |
| `main.py` | `update_entry()` used `if new_amount:` — falsy for `0` | Changed to `if new_amount is not None:` |
| `main.py` | `plot_transactions()` used wrong index for `reindex()`, misaligning chart data | Fixed to use `pd.date_range()` for clean daily index |
| `main.py` | Monthly plot showed net only instead of separate income/expense lines | Split into two `resample("ME")` series |
| `Requirement.txt.txt` | Double `.txt` extension, typo `matpolt` | Replaced with correct `requirements.txt` |
| `index.html` | Seeded with 16 demo transactions on load | Replaced with empty `transactions = []` — starts clean |
| `finance_data.csv` | Personal data committed to repo | Deleted from repo, now gitignored |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — free to use, modify, and distribute.
