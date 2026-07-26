import os
import pytest
from fastapi.testclient import TestClient
from server import app
from database import get_db, Base, engine

client = TestClient(app)

def test_api_categories_get():
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_api_transactions_crud():
    # 1. Create Transaction
    payload = {
        "date": "26-07-2026",
        "amount": 1500.0,
        "category": "Food",
        "description": "Lunch with team",
        "currency": "INR"
    }
    create_res = client.post("/api/transactions", json=payload)
    assert create_res.status_code == 200
    tx_data = create_res.json()
    assert tx_data["amount"] == 1500.0
    tx_id = tx_data["id"]

    # 2. Get Transactions
    get_res = client.get("/api/transactions")
    assert get_res.status_code == 200

    # 3. Update Transaction
    payload["amount"] = 1800.0
    update_res = client.put(f"/api/transactions/{tx_id}", json=payload)
    assert update_res.status_code == 200
    assert update_res.json()["amount"] == 1800.0

    # 4. Delete Transaction
    del_res = client.delete(f"/api/transactions/{tx_id}")
    assert del_res.status_code == 200

def test_category_referential_integrity_deletion_block():
    # Create test category
    cat_payload = {"name": "TestRefCat", "type": "Expense", "color": "#123456", "icon": "🧪"}
    cat_res = client.post("/api/categories", json=cat_payload)
    assert cat_res.status_code in (200, 400)
    
    # Fetch category ID
    cats = client.get("/api/categories").json()
    test_cat = next((c for c in cats if c["name"] == "TestRefCat"), None)
    assert test_cat is not None
    cat_id = test_cat["id"]

    # Create transaction referencing this category
    tx_payload = {"date": "26-07-2026", "amount": 500.0, "category": "TestRefCat", "description": "Ref test"}
    tx_res = client.post("/api/transactions", json=tx_payload)
    assert tx_res.status_code == 200
    tx_id = tx_res.json()["id"]

    # Deleting category should fail with 409 Conflict
    del_cat_res = client.delete(f"/api/categories/{cat_id}")
    assert del_cat_res.status_code == 409

    # Clean up transaction and then delete category
    client.delete(f"/api/transactions/{tx_id}")
    del_cat_res_ok = client.delete(f"/api/categories/{cat_id}")
    assert del_cat_res_ok.status_code == 200

def test_recurring_rule_process():
    # Create recurring rule
    rule_payload = {
        "description": "Gym Membership",
        "amount": 2000.0,
        "category": "Health",
        "frequency": "monthly",
        "next_date": "01-01-2026",
        "is_active": True
    }
    create_res = client.post("/api/recurring", json=rule_payload)
    assert create_res.status_code == 200
    rule_id = create_res.json()["id"]

    # Process recurring rules
    proc_res = client.post("/api/recurring/process")
    assert proc_res.status_code == 200
    assert proc_res.json()["processed_count"] >= 1

    # Clean up rule
    client.delete(f"/api/recurring/{rule_id}")

def test_export_pdf_excel_csv():
    assert client.get("/api/export/pdf").status_code == 200
    assert client.get("/api/export/excel").status_code == 200
    assert client.get("/api/export/csv").status_code == 200

def test_backup_endpoint():
    res = client.get("/api/backup")
    assert res.status_code == 200
    assert len(res.content) > 0
