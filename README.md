# Personal Finance Tracker

A Python CLI tool to track personal income and expenses, with an upgraded **web dashboard** (`fintrack.html`) that runs entirely in your browser — no server needed.

---

## Features

### CLI (`main.py`)
- Add, view, update, and delete transactions stored in `finance_data.csv`
- Filter transactions by date range
- Plot daily income vs expenses and monthly summaries using Matplotlib
- Export data to CSV

### Web Dashboard (`fintrack.html`)
- **Dashboard** — KPI cards, Income vs Expenses line chart (3M/6M/1Y/All), spending doughnut chart, recent transactions
- **Transactions** — sortable table, date/type/category filters, global search, inline edit & delete, CSV export
- **Analytics** — monthly bar chart (12 months), income & expense breakdowns by category with progress bars
- **Budgets** — set monthly limits per category with live progress bars and over-budget alerts
- **Dark / Light mode** toggle
- **Mobile responsive** — collapsible sidebar
- Currency formatted in Indian Rupees (₹)

---

## Setup (CLI)

```bash
pip install -r requirements.txt
python main.py
```

## Usage (Web Dashboard)

Open `fintrack.html` in any modern browser. No installation or server required.

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
