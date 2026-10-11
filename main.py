from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

@app.get("/hello")
def say_hello():
    return {"message": "Hello, Avinash."}


@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    return {
        "expense_id": expense_id,
        "message": "Expense retrieved successfully."
    }

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

@app.post("/expenses")
def create_expenses(expense: ExpenseCreate):
    return {
        "message": "Expense received successfully.",
        "expense": expense
    }
