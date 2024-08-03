import pandas as pd
import csv
from datetime import datetime, timedelta
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
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        cls.sort_csv_by_date()
        print("Entry added successfully")

    @classmethod
    def sort_csv_by_date(cls):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        df.sort_values(by="date", ascending=False, inplace=True)
        df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No transactions found in the given date range.')
        else:
            print(f"Transaction from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Saving: ${total_income - total_expense:.2f}")

        return filtered_df

    @classmethod
    def delete_entry(cls, date, description):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        date = datetime.strptime(date, CSV.FORMAT)
        mask = (df["date"] == date) & (df["description"] == description)
        if mask.any():
            df = df[~mask]
            df.to_csv(cls.CSV_FILE, index=False)
            print("Entry deleted successfully")
        else:
            print("No matching entry found to delete")

    @classmethod
    def update_entry(cls, date, description, new_amount=None, new_category=None, new_description=None):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        date = datetime.strptime(date, CSV.FORMAT)
        mask = (df["date"] == date) & (df["description"] == description)
        if mask.any():
            if new_amount:
                df.loc[mask, "amount"] = new_amount
            if new_category:
                df.loc[mask, "category"] = new_category
            if new_description:
                df.loc[mask, "description"] = new_description
            df.to_csv(cls.CSV_FILE, index=False)
            print("Entry updated successfully")
        else:
            print("No matching entry found to update")

    @classmethod
    def export_csv(cls, export_path):
        df = pd.read_csv(cls.CSV_FILE)
        df.to_csv(export_path, index=False)
        print(f"CSV file exported to {export_path}")

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_monthly_summary():
    df = pd.read_csv(CSV.CSV_FILE)
    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
    df.set_index("date", inplace=True)

    monthly_df = df.resample("M").sum()

    plt.figure(figsize=(10, 5))
    plt.plot(monthly_df.index, monthly_df["amount"], label="Net Amount", color="b")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.title("Monthly Net Amount Summary")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Delete a transaction")
        print("4. Update a transaction")
        print("5. Plot monthly summary")
        print("6. Export CSV file")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            date = get_date("Enter the date of the transaction to delete (dd-mm-yyyy): ")
            description = input("Enter the description of the transaction to delete: ")
            CSV.delete_entry(date, description)
        elif choice == "4":
            date = get_date("Enter the date of the transaction to update (dd-mm-yyyy): ")
            description = input("Enter the description of the transaction to update: ")
            new_amount = input("Enter the new amount (or leave blank to keep the current amount): ")
            new_category = input("Enter the new category (or leave blank to keep the current category): ")
            new_description = input("Enter the new description (or leave blank to keep the current description): ")
            CSV.update_entry(date, description, new_amount if new_amount else None, new_category if new_category else None, new_description if new_description else None)
        elif choice == "5":
            plot_monthly_summary()
        elif choice == "6":
            export_path = input("Enter the export file path (e.g., export.csv): ")
            CSV.export_csv(export_path)
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3, 4, 5, 6 or 7.")

if __name__ == "__main__":
    main()
