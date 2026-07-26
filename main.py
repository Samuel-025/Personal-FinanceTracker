import sys
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Rich Terminal UI Imports
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, FloatPrompt, IntPrompt
from rich.text import Text
from rich.align import Align
from rich import print as rprint

# Local DB & Model Imports
from database import init_db, SessionLocal
from models import Transaction, Category, Budget, RecurringRule
from data_entry import get_date, get_amount, get_description

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console()
CURRENCY_SYMBOLS = {"INR": "₹", "USD": "$", "EUR": "€"}


def get_db_session():
    return SessionLocal()


# ---------------------------------------------------------------------------
# CLI Helpers & Rendering
# ---------------------------------------------------------------------------
def display_header():
    console.print(
        Panel.fit(
            "[bold green]💰 Personal Finance Tracker V2[/bold green]\n"
            "[dim]Unified SQLite Backend & Rich Terminal Interface[/dim]",
            border_style="green",
            padding=(1, 4),
        )
    )


def print_kpis(transactions, categories):
    income_cats = [str(c.name) for c in categories if c.type == "Income"]
    total_inc = sum(float(getattr(t, "amount", 0.0)) for t in transactions if t.category in income_cats)
    total_exp = sum(float(getattr(t, "amount", 0.0)) for t in transactions if t.category not in income_cats)
    net_savings = total_inc - total_exp

    savings_style = "bold green" if net_savings >= 0 else "bold red"

    kpi_text = Text()
    kpi_text.append(f" Total Income:  ₹{total_inc:,.2f}  ", style="bold green")
    kpi_text.append(f"│  Total Expense: ₹{total_exp:,.2f}  ", style="bold red")
    kpi_text.append(f"│  Net Savings: ₹{net_savings:,.2f}", style=savings_style)

    console.print(Panel(kpi_text, title="Financial Summary", border_style="blue"))


def render_transactions_table(transactions, categories=None, title="Transactions"):
    if not transactions:
        console.print(Panel("[yellow]No transactions found.[/yellow]", border_style="yellow"))
        return

    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Date", style="cyan", width=12)
    table.add_column("Category", style="yellow")
    table.add_column("Type", style="bold")
    table.add_column("Amount", justify="right")
    table.add_column("Description", style="italic")

    if categories is None:
        db = get_db_session()
        try:
            categories = db.query(Category).all()
        finally:
            db.close()

    income_cats = [c.name for c in categories if c.type == "Income"]

    for t in transactions:
        is_inc = t.category in income_cats
        type_style = "[green]Income[/green]" if is_inc else "[red]Expense[/red]"
        sym = CURRENCY_SYMBOLS.get(str(t.currency or "INR"), "₹")
        amt = float(t.amount)
        amt_str = f"[green]+{sym}{amt:,.2f}[/green]" if is_inc else f"[red]-{sym}{amt:,.2f}[/red]"

        table.add_row(
            str(t.id),
            str(t.date),
            str(t.category),
            type_style,
            amt_str,
            str(t.description or "-"),
        )

    console.print(table)


# ---------------------------------------------------------------------------
# Menu Handlers
# ---------------------------------------------------------------------------
def add_transaction_cli():
    console.rule("[bold green]Add New Transaction[/bold green]")
    db = get_db_session()
    try:
        categories = db.query(Category).all()
        if not categories:
            console.print("[red]No categories found. Initializing database...[/red]")
            init_db()
            categories = db.query(Category).all()

        date = get_date(
            "Enter date (dd-mm-yyyy) or press Enter for today: ",
            allow_default=True,
        )

        # Select Category
        console.print("\n[bold cyan]Available Categories:[/bold cyan]")
        for idx, cat in enumerate(categories, 1):
            type_tag = f"[green]{cat.type}[/green]" if cat.type == "Income" else f"[red]{cat.type}[/red]"
            console.print(f" {idx}. {cat.icon} {cat.name} ({type_tag})")

        cat_choice = IntPrompt.ask(
            "Select category number", choices=[str(i) for i in range(1, len(categories) + 1)]
        )
        selected_cat = categories[cat_choice - 1].name

        amount = get_amount()
        description = get_description()

        currency = Prompt.ask("Select Currency", choices=["INR", "USD", "EUR"], default="INR")

        tx = Transaction(
            date=date,
            amount=amount,
            category=selected_cat,
            description=description,
            currency=currency,
        )
        db.add(tx)
        db.commit()
        console.print(f"[bold green]✓ Added transaction of ₹{amount:,.2f} under {selected_cat}![/bold green]")
    finally:
        db.close()


def view_transactions_cli():
    console.rule("[bold cyan]View Transactions & Summary[/bold cyan]")
    db = get_db_session()
    try:
        categories = db.query(Category).all()
        use_filter = Confirm.ask("Do you want to filter by date range?", default=False)
        
        start_date = None
        end_date = None
        if use_filter:
            start_date = get_date("Enter start date (dd-mm-yyyy): ")
            end_date = get_date("Enter end date (dd-mm-yyyy): ")

        transactions = db.query(Transaction).all()
        if start_date or end_date:
            fmt = "%d-%m-%Y"
            filtered = []
            for t in transactions:
                try:
                    t_date = datetime.strptime(t.date, fmt)
                    if start_date and t_date < datetime.strptime(start_date, fmt):
                        continue
                    if end_date and t_date > datetime.strptime(end_date, fmt):
                        continue
                    filtered.append(t)
                except ValueError:
                    filtered.append(t)
            transactions = filtered

        # Sort descending by date
        try:
            transactions.sort(key=lambda x: datetime.strptime(str(x.date), "%d-%m-%Y"), reverse=True)
        except Exception:
            pass

        print_kpis(transactions, categories)
        render_transactions_table(transactions, categories=categories)
    finally:
        db.close()


def update_transaction_cli():
    console.rule("[bold yellow]Update Transaction[/bold yellow]")
    db = get_db_session()
    try:
        transactions = db.query(Transaction).all()
        categories = db.query(Category).all()
        if not transactions:
            console.print("[yellow]No transactions available to update.[/yellow]")
            return

        render_transactions_table(transactions, categories=categories, title="Select Transaction ID to Update")
        tx_id = IntPrompt.ask("Enter Transaction ID to update")
        tx = db.query(Transaction).filter_by(id=tx_id).first()

        if not tx:
            console.print("[red]Transaction ID not found.[/red]")
            return

        tx_amt = float(getattr(tx, "amount", 0.0))
        tx_date = str(getattr(tx, "date", ""))
        tx_desc = str(getattr(tx, "description", ""))

        console.print(f"\n[dim]Updating Transaction #{tx.id} ({tx_date} - ₹{tx_amt})[/dim]")
        new_date = Prompt.ask("New date (dd-mm-yyyy) or press Enter to keep current", default=tx_date)
        new_amount_str = Prompt.ask("New amount or press Enter to keep current", default=str(tx_amt))
        try:
            new_amount = float(new_amount_str)
            if new_amount <= 0:
                console.print("[red]Amount must be a positive number greater than 0. Keeping previous amount.[/red]")
                new_amount = tx_amt
        except ValueError:
            console.print("[red]Invalid numerical amount. Keeping previous amount.[/red]")
            new_amount = tx_amt

        new_desc = Prompt.ask("New description or press Enter to keep current", default=tx_desc)

        tx.date = new_date
        tx.amount = new_amount
        tx.description = new_desc
        db.commit()
        console.print("[bold green]✓ Transaction updated successfully![/bold green]")
    finally:
        db.close()


def delete_transaction_cli():
    console.rule("[bold red]Delete Transaction[/bold red]")
    db = get_db_session()
    try:
        transactions = db.query(Transaction).all()
        if not transactions:
            console.print("[yellow]No transactions available to delete.[/yellow]")
            return

        render_transactions_table(transactions, title="Select Transaction ID to Delete")
        tx_id = IntPrompt.ask("Enter Transaction ID to delete")
        tx = db.query(Transaction).filter_by(id=tx_id).first()

        if not tx:
            console.print("[red]Transaction ID not found.[/red]")
            return

        tx_amt = float(getattr(tx, "amount", 0.0))
        tx_cat = str(getattr(tx, "category", ""))
        if Confirm.ask(f"Are you sure you want to delete transaction #{tx.id} ({tx_cat} ₹{tx_amt})?"):
            db.delete(tx)
            db.commit()
            console.print("[bold green]✓ Transaction deleted successfully![/bold green]")
    finally:
        db.close()


def category_manager_cli():
    console.rule("[bold magenta]Category Manager[/bold magenta]")
    db = get_db_session()
    try:
        categories = db.query(Category).all()
        table = Table(title="Categories", show_header=True, header_style="bold magenta")
        table.add_column("ID", width=4)
        table.add_column("Icon", width=6)
        table.add_column("Category Name", style="bold")
        table.add_column("Type", style="cyan")

        for c in categories:
            type_style = "[green]Income[/green]" if c.type == "Income" else "[red]Expense[/red]"
            table.add_row(str(c.id), c.icon, c.name, type_style)

        console.print(table)

        if Confirm.ask("\nDo you want to add a new custom category?", default=False):
            cat_name = Prompt.ask("Enter category name").strip()
            cat_type = Prompt.ask("Select category type", choices=["Income", "Expense"])
            icon = Prompt.ask("Enter emoji icon for category", default="📋")
            color = Prompt.ask("Enter hex color (e.g. #60a5fa)", default="#60a5fa")

            new_cat = Category(name=cat_name, type=cat_type, icon=icon, color=color)
            db.add(new_cat)
            db.commit()
            console.print(f"[bold green]✓ Category '{cat_name}' added successfully![/bold green]")
    finally:
        db.close()


def budget_manager_cli():
    console.rule("[bold blue]Budget Goals Manager[/bold blue]")
    db = get_db_session()
    try:
        budgets = db.query(Budget).all()
        now = datetime.now()
        this_month_str = now.strftime("%m-%Y")

        txs = db.query(Transaction).all()
        monthly_exp = {}
        for t in txs:
            try:
                cat_str = t.category
                d_str = t.date
                t_amt = float(getattr(t, "amount", 0.0))
                if d_str[-7:] == this_month_str:
                    monthly_exp[cat_str] = monthly_exp.get(cat_str, 0.0) + t_amt
            except Exception:
                pass

        if budgets:
            table = Table(title="Monthly Category Budgets", show_header=True)
            table.add_column("Category", style="bold")
            table.add_column("Monthly Limit", justify="right")
            table.add_column("Spent This Month", justify="right")
            table.add_column("Status")

            for b in budgets:
                cat_name_str = b.category_name
                limit_val = float(getattr(b, "monthly_limit", 0.0))
                spent = monthly_exp.get(cat_name_str, 0.0)
                over = spent > limit_val
                pct = min(int((spent / limit_val) * 100), 100) if limit_val > 0 else 0
                status_str = f"[red]OVER BUDGET! ({pct}%)[/red]" if over else f"[green]{pct}% used[/green]"
                table.add_row(
                    cat_name_str,
                    f"₹{limit_val:,.2f}",
                    f"₹{spent:,.2f}",
                    status_str,
                )
            console.print(table)
        else:
            console.print("[yellow]No budget goals set yet.[/yellow]")

        if Confirm.ask("\nDo you want to set/update a category budget?", default=False):
            exp_cats = [c.name for c in db.query(Category).filter_by(type="Expense").all()]
            console.print("\nAvailable Expense Categories:")
            for idx, name in enumerate(exp_cats, 1):
                console.print(f" {idx}. {name}")

            choice = IntPrompt.ask("Select category number", choices=[str(i) for i in range(1, len(exp_cats) + 1)])
            cat_name = exp_cats[choice - 1]
            limit = FloatPrompt.ask(f"Enter monthly spending limit for {cat_name} (₹)")

            b = db.query(Budget).filter_by(category_name=cat_name).first()
            if b:
                b.monthly_limit = limit
            else:
                b = Budget(category_name=cat_name, monthly_limit=limit)
                db.add(b)
            db.commit()
            console.print(f"[bold green]✓ Monthly budget set for {cat_name}: ₹{limit:,.2f}[/bold green]")
    finally:
        db.close()


def recurring_manager_cli():
    console.rule("[bold cyan]Recurring Transactions Manager[/bold cyan]")
    db = get_db_session()
    try:
        rules = db.query(RecurringRule).all()
        if rules:
            table = Table(title="Active Recurring Rules", show_header=True)
            table.add_column("ID", width=4)
            table.add_column("Description", style="bold")
            table.add_column("Amount", justify="right")
            table.add_column("Category")
            table.add_column("Frequency")
            table.add_column("Next Due Date")

            for r in rules:
                r_amt = float(getattr(r, "amount", 0.0))
                table.add_row(
                    str(r.id),
                    r.description,
                    f"₹{r_amt:,.2f}",
                    r.category,
                    r.frequency,
                    r.next_date,
                )
            console.print(table)
        else:
            console.print("[yellow]No recurring transaction rules defined.[/yellow]")

        if Confirm.ask("\nDo you want to add a new recurring rule?", default=False):
            desc = Prompt.ask("Enter description (e.g. Salary, Rent, Netflix)")
            amt = FloatPrompt.ask("Enter amount (₹)")
            cats = [c.name for c in db.query(Category).all()]
            cat = Prompt.ask("Select category", choices=cats)
            freq = Prompt.ask("Select frequency", choices=["monthly", "weekly"], default="monthly")
            next_date = get_date("Enter next due date (dd-mm-yyyy): ")

            rule = RecurringRule(
                description=desc,
                amount=amt,
                category=cat,
                frequency=freq,
                next_date=next_date,
            )
            db.add(rule)
            db.commit()
            console.print(f"[bold green]✓ Recurring rule '{desc}' added![/bold green]")
    finally:
        db.close()


def plot_charts_cli():
    console.rule("[bold blue]Visual Analytics Charts[/bold blue]")
    db = get_db_session()
    try:
        txs = db.query(Transaction).all()
        if not txs:
            console.print("[yellow]No transactions available for plotting.[/yellow]")
            return

        data = []
        for t in txs:
            data.append(
                {
                    "date": t.date,
                    "amount": t.amount,
                    "category": t.category,
                }
            )

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", dayfirst=True)
        df.set_index("date", inplace=True)

        categories = db.query(Category).all()
        income_cats = [c.name for c in categories if c.type == "Income"]

        df["type"] = df["category"].apply(lambda c: "Income" if c in income_cats else "Expense")

        inc_monthly = df[df["type"] == "Income"]["amount"].resample("ME").sum()
        exp_monthly = df[df["type"] == "Expense"]["amount"].resample("ME").sum()

        plt.figure(figsize=(10, 5))
        plt.plot(list(inc_monthly.index), list(inc_monthly.values), label="Income", color="g", marker="o")
        plt.plot(list(exp_monthly.index), list(exp_monthly.values), label="Expenses", color="r", marker="o")
        plt.xlabel("Month")
        plt.ylabel("Amount (₹)")
        plt.title("Monthly Income vs Expenses")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        console.print("[bold green]Displaying Matplotlib Chart Window...[/bold green]")
        plt.show()
    finally:
        db.close()


def export_reports_cli():
    console.rule("[bold green]Export Financial Reports[/bold green]")
    console.print("Available Export Options:")
    console.print(" 1. PDF Financial Report (.pdf)")
    console.print(" 2. Excel Spreadsheet (.xlsx)")
    console.print(" 3. CSV File (.csv)")

    choice = Prompt.ask("Select export format", choices=["1", "2", "3"])
    db = get_db_session()
    try:
        txs = db.query(Transaction).all()
        if choice == "1":
            from server import export_pdf
            res = export_pdf(db=db)
            out_file = f"Financial_Summary_{datetime.now().strftime('%Y%m%d')}.pdf"
            with open(out_file, "wb") as f:
                f.write(res.body)
            console.print(f"[bold green]✓ PDF report saved to {out_file}![/bold green]")
        elif choice == "2":
            from server import export_excel
            res = export_excel(db=db)
            out_file = f"Financial_Report_{datetime.now().strftime('%Y%m%d')}.xlsx"
            with open(out_file, "wb") as f:
                f.write(res.body)
            console.print(f"[bold green]✓ Excel spreadsheet saved to {out_file}![/bold green]")
        elif choice == "3":
            out_file = Prompt.ask("Enter export file path", default="export.csv")
            data = [
                {
                    "date": t.date,
                    "amount": t.amount,
                    "category": t.category,
                    "description": t.description,
                    "currency": t.currency,
                }
                for t in txs
            ]
            df = pd.DataFrame(data)
            df.to_csv(out_file, index=False)
            console.print(f"[bold green]✓ CSV file exported to {out_file}![/bold green]")
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Main Loop
# ---------------------------------------------------------------------------
def main():
    init_db()
    while True:
        console.clear()
        display_header()
        console.print("\n[bold]Select Option:[/bold]")
        console.print(" [bold green]1.[/bold green] Add a New Transaction")
        console.print(" [bold cyan]2.[/bold cyan] View Transactions & Summary")
        console.print(" [bold yellow]3.[/bold yellow] Update a Transaction")
        console.print(" [bold red]4.[/bold red] Delete a Transaction")
        console.print(" [bold magenta]5.[/bold magenta] Manage Categories")
        console.print(" [bold blue]6.[/bold blue] Manage Budget Goals")
        console.print(" [bold cyan]7.[/bold cyan] Manage Recurring Transactions")
        console.print(" [bold green]8.[/bold green] Plot Visual Charts")
        console.print(" [bold yellow]9.[/bold yellow] Export Reports (PDF / Excel / CSV)")
        console.print(" [bold dim]10.[/bold dim] Exit")

        choice = Prompt.ask("\nEnter choice", choices=[str(i) for i in range(1, 11)])

        if choice == "1":
            add_transaction_cli()
        elif choice == "2":
            view_transactions_cli()
        elif choice == "3":
            update_transaction_cli()
        elif choice == "4":
            delete_transaction_cli()
        elif choice == "5":
            category_manager_cli()
        elif choice == "6":
            budget_manager_cli()
        elif choice == "7":
            recurring_manager_cli()
        elif choice == "8":
            plot_charts_cli()
        elif choice == "9":
            export_reports_cli()
        elif choice == "10":
            console.print("\n[bold green]Goodbye! Thank you for using Personal Finance Tracker V2.[/bold green]")
            break

        Prompt.ask("\n[dim]Press Enter to return to main menu...[/dim]")


if __name__ == "__main__":
    main()
