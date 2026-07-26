import os
import csv
import sys
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Transaction, Category, Budget, RecurringRule

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATABASE_URL = "sqlite:///./finance.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DEFAULT_CATEGORIES = [
    {"name": "Salary", "type": "Income", "color": "#4ade80", "icon": "💼"},
    {"name": "Freelance", "type": "Income", "color": "#60a5fa", "icon": "💻"},
    {"name": "Investment", "type": "Income", "color": "#a78bfa", "icon": "📈"},
    {"name": "Business", "type": "Income", "color": "#fbbf24", "icon": "🏪"},
    {"name": "Other Income", "type": "Income", "color": "#34d399", "icon": "💰"},
    {"name": "Food", "type": "Expense", "color": "#f87171", "icon": "🍽"},
    {"name": "Transport", "type": "Expense", "color": "#fb923c", "icon": "🚗"},
    {"name": "Housing", "type": "Expense", "color": "#f472b6", "icon": "🏠"},
    {"name": "Utilities", "type": "Expense", "color": "#fbbf24", "icon": "💡"},
    {"name": "Healthcare", "type": "Expense", "color": "#ef4444", "icon": "🏥"},
    {"name": "Entertainment", "type": "Expense", "color": "#c084fc", "icon": "🎬"},
    {"name": "Shopping", "type": "Expense", "color": "#38bdf8", "icon": "🛍"},
    {"name": "Education", "type": "Expense", "color": "#818cf8", "icon": "📚"},
    {"name": "Travel", "type": "Expense", "color": "#2dd4bf", "icon": "✈"},
    {"name": "Other Expense", "type": "Expense", "color": "#9ca3af", "icon": "📋"},
]


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Seed default categories if none exist
        if db.query(Category).count() == 0:
            for cat_data in DEFAULT_CATEGORIES:
                db.add(Category(**cat_data))
            db.commit()

        # Migrate CSV to SQLite if CSV exists and transactions table is empty
        csv_path = "finance_data.csv"
        if os.path.exists(csv_path) and db.query(Transaction).count() == 0:
            try:
                df = pd.read_csv(csv_path)
                if not df.empty and "date" in df.columns:
                    for _, row in df.iterrows():
                        desc = str(row.get("description", ""))
                        if desc == "nan" or pd.isna(desc):
                            desc = ""
                        
                        raw_cat = str(row["category"])
                        cat_name = raw_cat
                        if raw_cat in ["Income", "Expense"] and desc:
                            cat_name = desc
                        elif raw_cat == "Income":
                            cat_name = "Other Income"
                        elif raw_cat == "Expense":
                            cat_name = "Other Expense"

                        tx = Transaction(
                            date=str(row["date"]),
                            amount=float(row["amount"]),
                            category=cat_name,
                            description=desc,
                            currency="INR",
                        )
                        db.add(tx)
                    db.commit()
                    print("Successfully auto-migrated finance_data.csv into SQLite database!")
            except Exception as e:
                print(f"CSV migration notice: {e}")

        # Auto-normalize any existing transactions with generic category names
        txs = db.query(Transaction).all()
        normalized = False
        for t in txs:
            if t.category in ["Income", "Expense"]:
                if t.description:
                    t.category = t.description
                    normalized = True
                elif t.category == "Income":
                    t.category = "Other Income"
                    normalized = True
                elif t.category == "Expense":
                    t.category = "Other Expense"
                    normalized = True
        if normalized:
            db.commit()

        # Ensure active sample transactions for current month exist in database
        today_str = datetime.now().strftime("%d-%m-%Y")
        today_month = datetime.now().strftime("%m-%Y")
        has_current_month = any(str(t.date).endswith(today_month) for t in txs)

        if not has_current_month:
            samples = [
                Transaction(date=today_str, amount=15000.0, category="Salary", description="Monthly Salary", currency="INR"),
                Transaction(date=today_str, amount=2500.0, category="Groceries", description="Supermarket Shopping", currency="INR"),
                Transaction(date=today_str, amount=1200.0, category="Utilities", description="Electricity Bill", currency="INR"),
                Transaction(date=today_str, amount=800.0, category="Food", description="Restaurant Dinner", currency="INR"),
            ]
            for sample in samples:
                db.add(sample)
            db.commit()
            print("Seeded active current month transactions into SQLite database!")
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
