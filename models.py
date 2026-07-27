from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[str] = mapped_column(String, index=True)  # Format: dd-mm-yyyy
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, default="")
    currency: Mapped[Optional[str]] = mapped_column(String, default="INR")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)  # "Income" or "Expense"
    color: Mapped[Optional[str]] = mapped_column(String, default="#60a5fa")
    icon: Mapped[Optional[str]] = mapped_column(String, default="📋")


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    monthly_limit: Mapped[float] = mapped_column(Float, nullable=False)


class RecurringRule(Base):
    __tablename__ = "recurring_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    frequency: Mapped[Optional[str]] = mapped_column(String, default="monthly")  # "monthly" or "weekly"
    next_date: Mapped[str] = mapped_column(String, nullable=False)  # Format: dd-mm-yyyy
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, default=True)
