from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.routers import transactions, categories
from app.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(transactions.router)
app.include_router(categories.router)


@app.get("/health", tags=["health"])
def health_check(session: Annotated[Session, Depends(get_db)]):
    session.execute(text("SELECT 1"))
    return {"status": "ok"}
