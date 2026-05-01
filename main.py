from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.database import Base, engine   
from app.api.v1.wallets import router as wallets_router
from app.api.v1.operations import router as operations_router
from app.api.v1.users import router as users_router

app = FastAPI()
app.include_router(wallets_router, prefix="/api/v1", tags=["wallets"])
app.include_router(operations_router, prefix="/api/v1", tags=["operations"])
app.include_router(users_router, prefix="/api/v1", tags=["users"])

# Static files - use absolute path
static_dir = Path(__file__).parent / "app" / "static"
app.mount("/static", StaticFiles(directory=str(static_dir), html=True), name="static")    

Base.metadata.create_all(bind=engine)





#       чтобы запустить  
#       python -m uvicorn main:app --reload  

#       для теста
#       python -m pytest

#       фронт
#       http://localhost:8000/static/index.html