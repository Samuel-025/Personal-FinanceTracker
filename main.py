import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
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
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, dayfirst=True)
        df.sort_values(by="date", ascending=False, inplace=True)
        # BUG FIX: convert back to string before saving, not datetime objects
        df["date"] = df["date"].dt.strftime(cls.FORMAT)
        df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, dayfirst=True)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(
                f"Transactions from {start_date.strftime(cls.FORMAT)} "
                f"to {end_date.strftime(cls.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False,
                    formatters={"date": lambda x: x.strftime(cls.FORMAT)},
                )
            )
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print(f"Total Income:  ₹{total_income:.2f}")
            print(f"Total Expense: ₹{total_expense:.2f}")
            print(f"Net Savings:   ₹{total_income - total_expense:.2f}")

        return filtered_df

    @classmethod
    def delete_entry(cls, date, description):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, dayfirst=True)
        date_dt = datetime.strptime(date, cls.FORMAT)
        mask = (df["date"] == date_dt) & (df["description"] == description)
        if mask.any():
            df = df[~mask]
            df["date"] = df["date"].dt.strftime(cls.FORMAT)
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
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, dayfirst=True)
        date_dt = datetime.strptime(date, cls.FORMAT)
        mask = (df["date"] == date_dt) & (df["description"] == description)
        if mask.any():
            # BUG FIX: use 'is not None' so that 0 is treated as a valid amount
            if new_amount is not None:
                df.loc[mask, "amount"] = new_amount
            if new_category is not None:
                df.loc[mask, "category"] = new_category
            if new_description is not None:
                df.loc[mask, "description"] = new_description
            df["date"] = df["date"].dt.strftime(cls.FORMAT)
            df.to_csv(cls.CSV_FILE, index=False)
            print("Entry updated successfully.")
        else:
            print("No matching entry found to update.")

    @classmethod
    def export_csv(cls, export_path):
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
    # BUG FIX: build a clean date range index, resample against it
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
    df = pd.read_csv(CSV.CSV_FILE)
    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT, dayfirst=True)
    df.set_index("date", inplace=True)

    income_monthly = df[df["category"] == "Income"]["amount"].resample("ME").sum()
    expense_monthly = df[df["category"] == "Expense"]["amount"].resample("ME").sum()

    plt.figure(figsize=(10, 5))
    plt.plot(income_monthly.index, income_monthly.values, label="Income", color="g", marker="o")
    plt.plot(expense_monthly.index, expense_monthly.values, label="Expenses", color="r", marker="o")
    plt.xlabel("Month")
    plt.ylabel("Amount (₹)")
    plt.title("Monthly Income vs Expenses")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
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
            new_category = input(
                "Enter the new category (or leave blank to keep current): "
            ).strip() or None
            new_description = input(
                "Enter the new description (or leave blank to keep current): "
            ).strip() or None
            new_amount = float(new_amount_str) if new_amount_str else None
            CSV.update_entry(date, description, new_amount, new_category, new_description)
        elif choice == "5":
            plot_monthly_summary()
        elif choice == "6":
            export_path = input("Enter the export file path (e.g., export.csv): ").strip()
            CSV.export_csv(export_path)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()
