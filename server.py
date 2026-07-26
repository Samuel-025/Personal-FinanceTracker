import os
import io
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import init_db, get_db, SessionLocal
from models import Transaction, Category, Budget, RecurringRule

# Report Generation Libraries
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

app = FastAPI(
    title="Personal Finance Tracker API",
    description="REST API for Personal Finance Tracker V2",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    init_db()


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------
class TransactionSchema(BaseModel):
    id: Optional[int] = None
    date: str
    amount: float
    category: str
    description: Optional[str] = ""
    currency: Optional[str] = "INR"

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    id: Optional[int] = None
    name: str
    type: str  # "Income" or "Expense"
    color: Optional[str] = "#60a5fa"
    icon: Optional[str] = "📋"

    class Config:
        from_attributes = True


class BudgetSchema(BaseModel):
    id: Optional[int] = None
    category_name: str
    monthly_limit: float

    class Config:
        from_attributes = True


class RecurringSchema(BaseModel):
    id: Optional[int] = None
    description: str
    amount: float
    category: str
    frequency: str = "monthly"  # "monthly" or "weekly"
    next_date: str
    is_active: bool = True

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Root Route: Serve Dashboard
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def read_root():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>Personal Finance Tracker V2 API Running</h1>")


# ---------------------------------------------------------------------------
# Transactions Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/transactions", response_model=List[TransactionSchema])
def get_transactions(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None,
    type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Transaction)
    if category:
        query = query.filter(Transaction.category == category)
    if type:
        income_cats = [c.name for c in db.query(Category).filter(Category.type == "Income").all()]
        if type == "Income":
            query = query.filter(Transaction.category.in_(income_cats))
        elif type == "Expense":
            query = query.filter(~Transaction.category.in_(income_cats))

    transactions = query.all()

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
        transactions.sort(
            key=lambda x: datetime.strptime(x.date, "%d-%m-%Y"), reverse=True
        )
    except Exception:
        pass

    return transactions


@app.post("/api/transactions", response_model=TransactionSchema)
def create_transaction(item: TransactionSchema, db: Session = Depends(get_db)):
    tx = Transaction(
        date=item.date,
        amount=item.amount,
        category=item.category,
        description=item.description or "",
        currency=item.currency or "INR",
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


@app.put("/api/transactions/{tx_id}", response_model=TransactionSchema)
def update_transaction(
    tx_id: int, item: TransactionSchema, db: Session = Depends(get_db)
):
    tx = db.query(Transaction).filter(Transaction.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    tx.date = item.date
    tx.amount = item.amount
    tx.category = item.category
    tx.description = item.description or ""
    if item.currency:
        tx.currency = item.currency
    db.commit()
    db.refresh(tx)
    return tx


@app.delete("/api/transactions/{tx_id}")
def delete_transaction(tx_id: int, db: Session = Depends(get_db)):
    tx = db.query(Transaction).filter(Transaction.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(tx)
    db.commit()
    return {"message": "Transaction deleted successfully"}


# ---------------------------------------------------------------------------
# Categories Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/categories", response_model=List[CategorySchema])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@app.post("/api/categories", response_model=CategorySchema)
def create_category(item: CategorySchema, db: Session = Depends(get_db)):
    existing = db.query(Category).filter(Category.name == item.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    cat = Category(
        name=item.name,
        type=item.type,
        color=item.color or "#60a5fa",
        icon=item.icon or "📋",
    )
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@app.delete("/api/categories/{cat_id}")
def delete_category(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(cat)
    db.commit()
    return {"message": "Category deleted successfully"}


# ---------------------------------------------------------------------------
# Budgets Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/budgets", response_model=List[BudgetSchema])
def get_budgets(db: Session = Depends(get_db)):
    return db.query(Budget).all()


@app.post("/api/budgets", response_model=BudgetSchema)
def set_budget(item: BudgetSchema, db: Session = Depends(get_db)):
    existing = (
        db.query(Budget)
        .filter(Budget.category_name == item.category_name)
        .first()
    )
    if existing:
        existing.monthly_limit = item.monthly_limit
        db.commit()
        db.refresh(existing)
        return existing
    b = Budget(category_name=item.category_name, monthly_limit=item.monthly_limit)
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


@app.delete("/api/budgets/{category_name}")
def delete_budget(category_name: str, db: Session = Depends(get_db)):
    b = db.query(Budget).filter(Budget.category_name == category_name).first()
    if not b:
        raise HTTPException(status_code=404, detail="Budget not found")
    db.delete(b)
    db.commit()
    return {"message": "Budget removed successfully"}


# ---------------------------------------------------------------------------
# Recurring Rules Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/recurring", response_model=List[RecurringSchema])
def get_recurring(db: Session = Depends(get_db)):
    return db.query(RecurringRule).all()


@app.post("/api/recurring", response_model=RecurringSchema)
def create_recurring(item: RecurringSchema, db: Session = Depends(get_db)):
    rule = RecurringRule(
        description=item.description,
        amount=item.amount,
        category=item.category,
        frequency=item.frequency or "monthly",
        next_date=item.next_date,
        is_active=item.is_active,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@app.delete("/api/recurring/{rule_id}")
def delete_recurring(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(RecurringRule).filter(RecurringRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Recurring rule not found")
    db.delete(rule)
    db.commit()
    return {"message": "Recurring rule deleted"}


@app.post("/api/recurring/process")
def process_recurring(db: Session = Depends(get_db)):
    today_str = datetime.today().strftime("%d-%m-%Y")
    today_dt = datetime.strptime(today_str, "%d-%m-%Y")

    rules = db.query(RecurringRule).filter(RecurringRule.is_active == True).all()
    created_txs = []

    for rule in rules:
        try:
            next_dt = datetime.strptime(rule.next_date, "%d-%m-%Y")
            while next_dt <= today_dt:
                # Add transaction
                tx = Transaction(
                    date=next_dt.strftime("%d-%m-%Y"),
                    amount=rule.amount,
                    category=rule.category,
                    description=f"[Recurring] {rule.description}",
                    currency="INR",
                )
                db.add(tx)
                created_txs.append(rule.description)

                # Increment next date
                if rule.frequency == "weekly":
                    next_dt += timedelta(days=7)
                else:  # monthly
                    # Add ~30 days
                    month = next_dt.month % 12 + 1
                    year = next_dt.year + (next_dt.month // 12)
                    day = min(next_dt.day, 28)
                    next_dt = datetime(year, month, day)

            rule.next_date = next_dt.strftime("%d-%m-%Y")
        except Exception as e:
            print(f"Error processing recurring rule {rule.id}: {e}")

    db.commit()
    return {"processed_count": len(created_txs), "items": created_txs}


# ---------------------------------------------------------------------------
# Export Endpoints (PDF, Excel, CSV)
# ---------------------------------------------------------------------------
@app.get("/api/export/excel")
def export_excel(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Transactions Report"

    # Header styles
    header_fill = PatternFill(
        start_color="1E293B", end_color="1E293B", fill_type="solid"
    )
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    center_align = Alignment(horizontal="center", vertical="center")

    headers = ["ID", "Date", "Category", "Amount (₹)", "Description", "Currency"]
    ws.append(headers)

    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_align

    # Data Rows
    thin_border = Border(
        left=Side(style="thin", color="E2E8F0"),
        right=Side(style="thin", color="E2E8F0"),
        top=Side(style="thin", color="E2E8F0"),
        bottom=Side(style="thin", color="E2E8F0"),
    )

    for tx in transactions:
        row = [tx.id, tx.date, tx.category, tx.amount, tx.description, tx.currency]
        ws.append(row)
        current_row = ws.max_row
        for col in range(1, len(headers) + 1):
            cell = ws.cell(row=current_row, column=col)
            cell.border = thin_border
            if col == 4:
                cell.number_format = "₹#,##0.00"

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"Financial_Report_{datetime.now().strftime('%Y%m%d')}.xlsx"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(
        output,
        headers=headers,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@app.get("/api/export/pdf")
def export_pdf(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=12,
    )

    elements.append(Paragraph("💰 Personal Finance Summary Report", title_style))
    elements.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d %B %Y, %H:%M')}",
            styles["Normal"],
        )
    )
    elements.append(Spacer(1, 16))

    # Table Header
    data = [["Date", "Category", "Amount (₹)", "Description"]]

    total_inc = 0
    total_exp = 0

    income_cats = [c.name for c in db.query(Category).filter(Category.type == "Income").all()]

    for tx in transactions:
        if tx.category in income_cats:
            total_inc += tx.amount
        else:
            total_exp += tx.amount
        data.append([tx.date, tx.category, f"₹{tx.amount:,.2f}", tx.description or "-"])

    t = Table(data, colWidths=[80, 100, 100, 240])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("ALIGN", (2, 0), (2, -1), "RIGHT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ]
        )
    )

    elements.append(t)
    elements.append(Spacer(1, 20))

    # Summary Section
    summary_text = (
        f"<b>Total Income:</b> ₹{total_inc:,.2f} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<b>Total Expenses:</b> ₹{total_exp:,.2f} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<b>Net Savings:</b> ₹{total_inc - total_exp:,.2f}"
    )
    elements.append(Paragraph(summary_text, styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    filename = f"Financial_Summary_{datetime.now().strftime('%Y%m%d')}.pdf"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(
        buffer, headers=headers, media_type="application/pdf"
    )


@app.get("/api/export/csv")
def export_csv_api(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["date", "amount", "category", "description", "currency"])

    for tx in transactions:
        writer.writerow([tx.date, tx.amount, tx.category, tx.description, tx.currency])

    mem = io.BytesIO()
    mem.write(output.getvalue().encode("utf-8"))
    mem.seek(0)

    filename = f"finance_data_export_{datetime.now().strftime('%Y%m%d')}.csv"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(
        mem, headers=headers, media_type="text/csv"
    )
