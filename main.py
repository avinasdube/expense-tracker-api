from fastapi import FastAPI
from pydantic import BaseModel, Field

from decimal import Decimal

from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from database import Base, SessionLocal, engine
from models import Expense

app = FastAPI()

@app.get("/hello")
def say_hello():
    return {"message": "Hello, Avinash."}

@app.get("/search")
def search_expenses(category: str, limit: int = 100):
    return {
        "category": category,
        "limit": limit
    }

class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length = 200)


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.post("/expenses", status_code=201)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
):
    db_expense = Expense(
        amount = Decimal(str(expense.amount)),
        category = expense.category,
        description = expense.description,
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return {
        "id": db_expense.id,
        "amount": float(db_expense.amount),
        "category": db_expense.category,
        "description": db_expense.description,
    }


@app.get("/expenses")
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.scalars(select(Expense)).all()

    return [
        {
            "id": expense.id,
            "amount": float(expense.amount),
            "category": expense.category,
            "description": expense.description,
        }

        for expense in expenses
    ]

@app.get("/expenses/{expense_id}")
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    expense = db.get(Expense, expense_id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    return {
        "id": expense.id,
        "amount": float(expense.amount),
        "category": expense.category,
        "description": expense.description
    }
