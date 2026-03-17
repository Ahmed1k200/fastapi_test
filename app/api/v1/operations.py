from fastapi import APIRouter, HTTPException
from app.schemas import OperationRequest
from app.service import operations as operations_service

router = APIRouter()


@router.post("/operations/income")
def add_income(operarion: OperationRequest):
    return operations_service.add_income(operarion)

@router.post("/operations/expense")
def add_expense(operarion: OperationRequest):
    return operations_service.add_expense(operarion)