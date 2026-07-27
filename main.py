import pandas as pd
import csv
import sys
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        cls.initialize_csv()
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        cls.sort_csv_by_date()
        print("Entry added successfully.")

    @classmethod
    def sort_csv_by_date(cls):
        """Sort CSV by date descending. Preserves string format to avoid corruption."""
        cls.initialize_csv()
        df = pd.read_csv(cls.CSV_FILE)
        if df.empty:
            return
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, dayfirst=True)
        df.sort_values(by="date", ascending=False, inplace=True)
        df["date"] = df["date"].apply(
            lambda x: x.strftime(cls.FORMAT) if hasattr(x, "strftime") else str(x)
        )
        df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def get_transactions(cls, start_date, end_date):
        cls.initialize_csv()
        df = pd.read_csv(cls.CSV_FILE)
        if df.empty:
            print("No transactions found in the given date range.")
            return df
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, dayfirst=True)
        start_dt = datetime.strptime(start_date, cls.FORMAT)
        end_dt = datetime.strptime(end_date, cls.FORMAT)
        mask = (df["date"] >= start_dt) & (df["date"] <= end_dt)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(
                f"Transactions from {start_dt.strftime(cls.FORMAT)} "
                f"to {end_dt.strftime(cls.FORMAT)}"
            )
            display_df = filtered_df.copy()
            display_df["date"] = display_df["date"].apply(
                lambda x: x.strftime(cls.FORMAT) if hasattr(x, "strftime") else str(x)
            )
            print(display_df.to_string(index=False))
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print(f"Total Income:  ₹{total_income:.2f}")
            print(f"Total Expense: ₹{total_expense:.2f}")
            print(f"Net Savings:   ₹{total_income - total_expense:.2f}")

        return filtered_df

    @classmethod
    def delete_entry(cls, date, description):
        cls.initialize_csv()
        df = pd.read_csv(cls.CSV_FILE)
        if df.empty:
            print("No matching entry found to delete.")
            return
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, dayfirst=True)
        date_dt = datetime.strptime(date, cls.FORMAT)
        # Handle NaN descriptions read from empty CSV cells
        desc_clean = df["description"].fillna("")
        mask = (df["date"] == date_dt) & (desc_clean == description)
        if mask.any():
            df = df[~mask]
            if not df.empty:
                df["date"] = df["date"].apply(
                    lambda x: x.strftime(cls.FORMAT) if hasattr(x, "strftime") else str(x)
                )
            df.to_csv(cls.CSV_FILE, index=False)
            print("Entry deleted successfully.")
        else:
            print("No matching entry found to delete.")

    @classmethod
    def update_entry(
        cls,
        date,
        description,
        new_amount=None,
        new_category=None,
        new_description=None,
    ):
        cls.initialize_csv()
        df = pd.read_csv(cls.CSV_FILE)
        if df.empty:
            print("No matching entry found to update.")
            return
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, dayfirst=True)
        date_dt = datetime.strptime(date, cls.FORMAT)
        desc_clean = df["description"].fillna("")
        mask = (df["date"] == date_dt) & (desc_clean == description)
        if mask.any():
            if new_amount is not None:
                df.loc[mask, "amount"] = new_amount
            if new_category is not None:
                df.loc[mask, "category"] = new_category
            if new_description is not None:
                df.loc[mask, "description"] = new_description
            df["date"] = df["date"].apply(
                lambda x: x.strftime(cls.FORMAT) if hasattr(x, "strftime") else str(x)
            )
            df.to_csv(cls.CSV_FILE, index=False)
            print("Entry updated successfully.")
        else:
            print("No matching entry found to update.")

    @classmethod
    def export_csv(cls, export_path):
        cls.initialize_csv()
        df = pd.read_csv(cls.CSV_FILE)
        df.to_csv(export_path, index=False)
        print(f"CSV exported to {export_path}")


def add():
    CSV.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or press Enter for today: ",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    """Plot daily income and expense over the given date range."""
    if df is None or df.empty:
        print("No transaction data available to plot.")
        return

    df = df.copy()
    df.set_index("date", inplace=True)

    date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq="D")

    income_df = (
        df[df["category"] == "Income"]["amount"]
        .resample("D")
        .sum()
        .reindex(date_range, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]["amount"]
        .resample("D")
        .sum()
        .reindex(date_range, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df.values, label="Income", color="g")
    plt.plot(expense_df.index, expense_df.values, label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount (₹)")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_monthly_summary():
    CSV.initialize_csv()
    df = pd.read_csv(CSV.CSV_FILE)
    if df.empty:
        print("No transactions available to plot monthly summary.")
        return

    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT, dayfirst=True)
    df.set_index("date", inplace=True)

    income_monthly = df[df["category"] == "Income"]["amount"].resample("ME").sum()
    expense_monthly = df[df["category"] == "Expense"]["amount"].resample("ME").sum()

    plt.figure(figsize=(10, 5))
    plt.plot(income_monthly.index.tolist(), income_monthly.values.tolist(), label="Income", color="g", marker="o")
    plt.plot(expense_monthly.index.tolist(), expense_monthly.values.tolist(), label="Expenses", color="r", marker="o")
    plt.xlabel("Month")
    plt.ylabel("Amount (₹)")
    plt.title("Monthly Income vs Expenses")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    CSV.initialize_csv()
    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Delete a transaction")
        print("4. Update a transaction")
        print("5. Plot monthly summary")
        print("6. Export CSV file")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if not df.empty and input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            date = get_date("Enter the date of the transaction to delete (dd-mm-yyyy): ")
            description = input("Enter the description of the transaction to delete: ")
            CSV.delete_entry(date, description)
        elif choice == "4":
            date = get_date("Enter the date of the transaction to update (dd-mm-yyyy): ")
            description = input("Enter the description of the transaction to update: ")
            new_amount_str = input(
                "Enter the new amount (or leave blank to keep current): "
            ).strip()
            new_amount = None
            if new_amount_str:
                try:
                    new_amount = float(new_amount_str)
                    if new_amount <= 0:
                        print("Amount must be positive. Skipping amount update.")
                        new_amount = None
                except ValueError:
                    print("Invalid amount entered. Skipping amount update.")
                    new_amount = None

            new_category = input(
                "Enter the new category ('I' for Income, 'E' for Expense, or leave blank to keep current): "
            ).strip().upper()
            if new_category in ["I", "INCOME"]:
                new_category = "Income"
            elif new_category in ["E", "EXPENSE"]:
                new_category = "Expense"
            else:
                new_category = None

            new_description = input(
                "Enter the new description (or leave blank to keep current): "
            ).strip() or None

            CSV.update_entry(date, description, new_amount, new_category, new_description)
        elif choice == "5":
            plot_monthly_summary()
        elif choice == "6":
            export_path = input("Enter the export file path (e.g., export.csv): ").strip()
            if not export_path:
                export_path = "export.csv"
            CSV.export_csv(export_path)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()
