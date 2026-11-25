from fastapi import Depends, FastAPI, HTTPException, Path
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance API")


@app.post("/expenses", response_model=schemas.ExpenseRead, status_code=201)
def create_expense(data: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    expense = models.Expense(**data.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@app.get("/expenses", response_model=list[schemas.ExpenseRead])
def list_expenses(db: Session = Depends(get_db)):
    return db.query(models.Expense).all()


@app.get("/expenses/{expense_id}", response_model=schemas.ExpenseRead)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.get(models.Expense, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    return expense


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.get(models.Expense, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    db.delete(expense)
    db.commit()


@app.get("/summary/{year}/{month}")
def monthly_summary(
    year: int,
    month: int = Path(ge=1, le=12),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(models.Expense.category, func.sum(models.Expense.amount))
        .filter(
            extract("year", models.Expense.date) == year,
            extract("month", models.Expense.date) == month,
        )
        .group_by(models.Expense.category)
        .all()
    )
    by_category = {category: round(total, 2) for category, total in rows}
    return {
        "year": year,
        "month": month,
        "total": round(sum(by_category.values()), 2),
        "by_category": by_category,
    }