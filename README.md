# Personal Finance Tracker

A dual-mode personal finance tracker: a **Python CLI** for local use and a **full web app** for browser-based tracking.

**[Live Demo](https://samuel-025.github.io/Personal-FinanceTracker/)**

---

## Features

### Web App (`index.html`)
- **Dashboard** — KPI cards, Income vs Expense line chart (3M/6M/1Y/All), spending doughnut, recent transactions
- **Add Transaction** — validated form with 12 granular categories (Salary, Food, Transport, etc.)
- **Transactions** — sortable table, date/type/category filters, global search, inline edit & delete, CSV export
- **Analytics** — monthly bar chart, income & expense breakdown pies, category progress bars
- **Budgets** — set monthly spending limits per category with color-coded progress tracking
- **Dark / Light mode** toggle
- **Mobile responsive** with slide-out sidebar

### Python CLI (`main.py` + `data_entry.py`)
- Add, view, update, delete transactions stored in `finance_data.csv`
- Date-range filtered views with income/expense summary
- Matplotlib charts: Income vs Expense over time, Monthly bar chart
- CSV export

---

## Bugs Fixed

| File | Bug | Fix |
|------|-----|-----|
| `main.py` | `sort_csv_by_date()` saved datetime objects instead of `dd-mm-yyyy` strings, corrupting the CSV | Added `.dt.strftime(cls.FORMAT)` before `to_csv()` |
| `main.py` | `update_entry()` used `if new_amount:` which is falsy for `0` | Changed to `if new_amount is not None:` |
| `main.py` | `plot_transactions()` reindexed to raw transaction index instead of a daily date range | Fixed to use `pd.date_range(min, max, freq="D")` |
| `main.py` | `plot_monthly_summary()` summed all categories together | Split into separate income/expense bar chart |
| `data_entry.py` | Typo: `"Invalid date frmat. Please entr..."` | Corrected |
| `data_entry.py` | Error said `"Account must be..."` instead of `"Amount must be..."` | Corrected |
| `index.html` | Chart canvas destroyed via `innerHTML` on empty state causing `TypeError` crash on revisit | Replaced with show/hide sibling `<div>` pattern |
| `index.html` | Mobile sidebar had no backdrop click-to-close | Added backdrop overlay |
| `index.html` | Redundant `card.style.display="block"` before `resetAddForm()` | Removed |
| `index.html` | Unused `let ok = true` variables | Removed |
| `Requirement.txt.txt` | Double `.txt` extension; typo `matpolt` | Renamed to `requirements.txt`, corrected |

---

## Quick Start

### Web App
Open `index.html` in any browser — no installation required.

### Python CLI
```bash
pip install -r requirements.txt
python main.py
```

---

## Project Structure

```
Personal-FinanceTracker/
├── index.html          # Full-featured web app (single file, zero dependencies)
├── main.py             # Python CLI — transaction management + charts
├── data_entry.py       # Python CLI — input validation helpers
├── finance_data.csv    # CSV data store (auto-created if missing)
└── requirements.txt    # Python dependencies
```

---

## Tech Stack

| Layer | Web App | Python CLI |
|-------|---------|------------|
| Language | HTML / CSS / Vanilla JS | Python 3.8+ |
| Charts | Chart.js 4.4 | Matplotlib |
| Data | In-browser | CSV via Pandas |
| Styling | Custom CSS (dark/light mode) | Terminal |
