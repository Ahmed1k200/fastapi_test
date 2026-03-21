from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=50)
    amount: Decimal
    description: str | None = Field(None, max_length=200)

    @field_validator("amount")
    def validate_amount(cls, v: Decimal) -> Decimal:
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
    initial_balance: Decimal = 0

    @field_validator("name")
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Wallet name cannot be empty")
        return v
    
    @field_validator("initial_balance")
    def validate_initial_balance(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Initial balance must be a positive number")
        return v