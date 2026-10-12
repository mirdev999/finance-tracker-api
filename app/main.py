from fastapi import FastAPI, Depends
from app.routers import transactions
from app.config import settings
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

app = FastAPI(title=settings.app_name)

app.include_router(transactions.router)


@app.get("/health", tags=["health"])
def health_check(session: Annotated[Session, Depends(get_db)]):
    session.execute(text("SELECT 1"))
    return {"status": "ok"}
