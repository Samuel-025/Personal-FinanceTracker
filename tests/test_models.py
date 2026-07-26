import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Transaction, Category, Budget, RecurringRule

def test_models_instantiation():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    cat = Category(name="Salary", type="Income", color="#4ade80", icon="💼")
    session.add(cat)
    session.commit()

    tx = Transaction(date="26-07-2026", amount=5000.0, category="Salary", description="Paycheck", currency="INR")
    session.add(tx)
    session.commit()

    budget = Budget(category_name="Groceries", monthly_limit=15000.0)
    session.add(budget)
    session.commit()

    rule = RecurringRule(description="Netflix", amount=649.0, category="Entertainment", frequency="monthly", next_date="01-08-2026")
    session.add(rule)
    session.commit()

    assert session.query(Category).count() == 1
    assert session.query(Transaction).count() == 1
    assert session.query(Budget).count() == 1
    assert session.query(RecurringRule).count() == 1
    session.close()
