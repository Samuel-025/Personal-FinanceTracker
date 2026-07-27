from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)  # Format: dd-mm-yyyy
    amount = Column(Float, nullable=False)
    category = Column(String, index=True, nullable=False)
    description = Column(String, default="")
    currency = Column(String, default="INR")
    created_at = Column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    type = Column(String, nullable=False)  # "Income" or "Expense"
    color = Column(String, default="#60a5fa")
    icon = Column(String, default="📋")


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, unique=True, nullable=False)
    monthly_limit = Column(Float, nullable=False)


class RecurringRule(Base):
    __tablename__ = "recurring_rules"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    frequency = Column(String, default="monthly")  # "monthly" or "weekly"
    next_date = Column(String, nullable=False)  # Format: dd-mm-yyyy
    is_active = Column(Boolean, default=True)
