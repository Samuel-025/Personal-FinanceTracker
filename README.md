# Personal Finance Tracker

A Python CLI tool to track personal income and expenses, with an upgraded **web dashboard** (`personal-finance-tracker.html`) that runs entirely in your browser — no server needed.

---

## Live Demo

If GitHub Pages is enabled, open: https://samuel-025.github.io/Personal-FinanceTracker/

Or open personal-finance-tracker.html directly in any modern browser — no installation or server required.

---

## Features

### CLI (`main.py`)
- Add, view, update, and delete transactions stored in `finance_data.csv`
- Filter transactions by date range
- Plot daily income vs expenses and monthly summaries using Matplotlib
- Export data to CSV

### Web Dashboard (`personal-finance-tracker.html`)
- **Dashboard** — KPI cards, Income vs Expenses line chart (3M/6M/1Y/All), spending doughnut chart, recent transactions
- **Transactions** — sortable table, date/type/category filters, global search, inline edit & delete, CSV export
- **Analytics** — monthly bar chart (12 months), income & expense breakdowns by category with progress bars
- **Budgets** — set monthly limits per category with live progress bars and over-budget alerts
- **Dark / Light mode** toggle
- **Mobile responsive** — collapsible sidebar
- Currency formatted in Indian Rupees (₹)

> **Note:** The web dashboard stores data in memory only. All transactions reset on page refresh. For persistent data use the CLI with `finance_data.csv`.

---

## Setup (CLI)

```bash
pip install -r requirements.txt
python main.py
```

## Usage (Web Dashboard)

Open `personal-finance-tracker.html` in any modern browser. No installation or server required.

---

## Project Structure

```
Personal-FinanceTracker/
├── main.py                        # CLI app — add/view/update/delete/plot transactions
├── data_entry.py                  # Input helpers and validators for CLI
├── requirements.txt               # Python dependencies (pandas, matplotlib)
├── personal-finance-tracker.html  # Full web dashboard (no server needed)
├── index.html                     # Redirect to web dashboard
└── README.md
```

---

## Bug Fixes

| File | Bug | Fix |
|---|---|---|
| `data_entry.py` | Typos in error messages (`frmat`, `entr`, `Account`) | Corrected all three |
| `main.py` | `sort_csv_by_date()` saved datetime objects instead of strings, corrupting CSV on next read | Added `.dt.strftime()` conversion before saving |
| `main.py` | `update_entry()` used `if new_amount:` — falsy for `0` | Changed to `if new_amount is not None:` |
| `main.py` | `plot_transactions()` used wrong index source for `reindex()`, misaligning chart data | Fixed to use `pd.date_range()` for a clean daily index |
| `main.py` | Monthly plot only showed net amount instead of separate income/expense lines | Split into two `resample("ME")` series |
| `Requirement.txt.txt` | Double `.txt` extension, typo `matpolt` | Replaced with `requirements.txt` |
| `index.html` | Empty placeholder file | Filled with meta-refresh redirect to dashboard |
| `fintrack.html` | Duplicate of main dashboard | Removed — `personal-finance-tracker.html` is canonical |
