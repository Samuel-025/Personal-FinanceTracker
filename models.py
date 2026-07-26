from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id: int = Column(Integer, primary_key=True, index=True)
    date: str = Column(String, index=True)  # Format: dd-mm-yyyy
    amount: float = Column(Float, nullable=False)
    category: str = Column(String, index=True, nullable=False)
    description: str = Column(String, default="")
    currency: str = Column(String, default="INR")
    created_at = Column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, index=True, nullable=False)
    type: str = Column(String, nullable=False)  # "Income" or "Expense"
    color: str = Column(String, default="#60a5fa")
    icon: str = Column(String, default="📋")


class Budget(Base):
    __tablename__ = "budgets"

    id: int = Column(Integer, primary_key=True, index=True)
    category_name: str = Column(String, unique=True, nullable=False)
    monthly_limit: float = Column(Float, nullable=False)


class RecurringRule(Base):
    __tablename__ = "recurring_rules"

    id: int = Column(Integer, primary_key=True, index=True)
    description: str = Column(String, nullable=False)
    amount: float = Column(Float, nullable=False)
    category: str = Column(String, nullable=False)
    frequency: str = Column(String, default="monthly")  # "monthly" or "weekly"
    next_date: str = Column(String, nullable=False)  # Format: dd-mm-yyyy
    is_active: bool = Column(Boolean, default=True)
