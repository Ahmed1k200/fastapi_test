from fastapi import HTTPException, APIRouter
from app.schemas import OperationRequest
from app.repository import wallets as wallets_repository


def add_income(operarion: OperationRequest):
    if not wallets_repository.is_wallet_exists(operarion.wallet_name):
        raise HTTPException(
            status_code=404, 
            detail=f"Wallet {operarion.wallet_name} not found"
        )
    new_balance = wallets_repository.add_income(operarion.wallet_name, operarion.amount)
    return{
        "message": "income added",
        "wallet": operarion.wallet_name,
        "amount": operarion.amount,
        "description": operarion.description,
        "new_balance": new_balance       
    }

def add_expense(operarion: OperationRequest):
    if not wallets_repository.is_wallet_exists(operarion.wallet_name):
        raise HTTPException(
            status_code=404, 
            detail=f"Wallet {operarion.wallet_name} not found"
        )
    
    balance = wallets_repository.get_wallet_balance_by_name(operarion.wallet_name)
    if operarion.amount <= 0:
        raise HTTPException(
            status_code=400, 
            detail="Amount must be greater than zero"
        )
    if balance < operarion.amount:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient balance. Available balance: {balance}"
        )
    new_balance = wallets_repository.add_expense(operarion.wallet_name, operarion.amount)
    return{
        "message": "Expense added",
        "wallet": operarion.wallet_name,
        "amount": operarion.amount,
        "description": operarion.description,
        "new_balance": new_balance       
    }