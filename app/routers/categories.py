from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Transaction, Category
from app.schemas import TransactionOut, TransactionCreate, CategoryOut, CategoryCreate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", status_code=201, response_model=CategoryOut)
def create_category(
    category_in: CategoryCreate, session: Annotated[Session, Depends(get_db)]
):
    dict_cat_in = category_in.model_dump()
    input_cat_name = dict_cat_in["name"].strip().lower()
    if len(input_cat_name) == 0:
        raise HTTPException(status_code=422, detail="category name cannot be empty")
    existing_category = session.scalars(
        select(Category).where(Category.name == input_cat_name)
    ).first()
    if existing_category is not None:
        raise HTTPException(
            status_code=409, detail="category name already exist,duplicated not allowed"
        )
    new_category = Category(name=input_cat_name)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category


@router.get("", response_model=list[CategoryOut])
def list_categories(session: Annotated[Session, Depends(get_db)]):
    return session.scalars(select(Category).order_by(Category.name.asc())).all()
