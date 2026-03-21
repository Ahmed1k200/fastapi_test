from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from app.database import Base, engine   
from app.api.v1.wallets import router as wallets_router
from app.api.v1.operations import router as operations_router

app = FastAPI()
app.include_router(wallets_router, prefix="/api/v1", tags=["wallets"])
app.include_router(operations_router, prefix="/api/v1", tags=["operations"])


Base.metadata.create_all(bind=engine)







#       python -m uvicorn main:app --reload