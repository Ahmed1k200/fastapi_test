from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator  

app = FastAPI()

BALANCE = {}

class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=50)
    amount: float
    description: str | None = Field(None, max_length=200)

    @field_validator("amount")
    def validate_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than zero")
        return v
    
    @field_validator("wallet_name")
    def wallet_name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Wallet name cannot be empty")
        return v

class CreateWalletRequest(BaseModel):
    name: str = Field(..., max_length=50)
    initial_balance: float = 0

    @field_validator("name")
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Wallet name cannot be empty")
        return v
    
    @field_validator("initial_balance")
    def validate_initial_balance(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Initial balance must be a positive number")
        return v

@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    if wallet_name is None:
        return{"total_balance": sum(BALANCE.values())}     
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404, 
            detail=f"Wallet {wallet_name} not found"
        )
    return {
        "wallet_name": wallet_name, 
        "balance": BALANCE[wallet_name]
    }

@app.post("/wallets")
def create_wallet(wallet: CreateWalletRequest):
    if wallet.name in BALANCE:
        raise HTTPException(
            status_code=400, 
            detail=f"Wallet {wallet.name} already exists"
        )
    BALANCE[wallet.name] = wallet.initial_balance
    return {
        "message": f"wallet {wallet.name} created",
        "wallet": wallet.name, 
        "balance": BALANCE[wallet.name]
    }

@app.post("/operations/income")
def add_income(operarion: OperationRequest):
    if operarion.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=400, 
            detail=f"Wallet {operarion.wallet_name} not found"
        )
    BALANCE[operarion.wallet_name] += operarion.amount
    return{
        "message": "income added",
        "wallet": operarion.wallet_name,
        "amount": operarion.amount,
        "description": operarion.description,
        "new_balance": BALANCE[operarion.wallet_name]       
    }

@app.post("/operations/expense")
def add_expense(operarion: OperationRequest):
    if operarion.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=400, 
            detail=f"Wallet {operarion.wallet_name} not found"
        )
    if operarion.amount <= 0:
        raise HTTPException(
            status_code=400, 
            detail="Amount must be greater than zero"
        )
    if BALANCE[operarion.wallet_name] < operarion.amount:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient balance. Available balance: {BALANCE[operarion.wallet_name]}"
        )
    BALANCE[operarion.wallet_name] -= operarion.amount
    return{
        "message": "Expense added",
        "wallet": operarion.wallet_name,
        "amount": operarion.amount,
        "description": operarion.description,
        "new_balance": BALANCE[operarion.wallet_name]       
    }