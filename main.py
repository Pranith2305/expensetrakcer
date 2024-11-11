from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import database
from models import expenses

app = FastAPI()

class ExpenseIn(BaseModel):
    title: str  # Title of the expense (required)
    amount: float  # Amount spent (required)
    category: str = None  # Optional category for the expense

class ExpenseOut(BaseModel):
    id : int
    title : str
    amount : float
    category : str
    created_at : str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post('/expenses/', response_model= ExpenseOut )
async def create_expenses(expense : ExpenseIn):
    query = expenses.insert().values(
        title = expense.title,
        amount = expense.amount,
        category = expense.category
    )

    last_record_id = await database.execute(query)
    return {**expense.dict(), "id": last_record_id, "created_at": "now"}

@app.get('/expenses/', response_model=List[ExpenseOut])
async def read_expenses():
    query = expenses.select()
    return await database.fetch_all(query)

@app.get('/expenses/{expense_id}', response_model=ExpenseOut)
async def read_expense(expense_id : int):
    query = expenses.select().where(expenses.c.id == expense_id)
    expense = await database.fetch_one(query)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense
@app.delete('/expenses/{expense_id}', status_code=200)
async def delete_expense(expense_id : int):
    query = expenses.delete().where(expenses.c.id == expense_id)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message" : "Expense deleted successfully"}

