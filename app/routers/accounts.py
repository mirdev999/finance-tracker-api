from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Account
from app.schemas import AccountCreate, AccountOut

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", status_code=201, response_model=AccountOut)
def create_account(
    account_in: AccountCreate, session: Annotated[Session, Depends(get_db)]
):
    dict_acc_in = account_in.model_dump()
    input_acc_name = dict_acc_in["name"].strip().lower()
    if len(input_acc_name) == 0:
        raise HTTPException(status_code=422, detail="Account name cannot be empty")
    existing_account = session.scalars(
        select(Account).where(Account.name == input_acc_name)
    ).first()
    if existing_account is not None:
        raise HTTPException(status_code=409, detail="Account already exists")
    new_account = Account(name=input_acc_name)
    session.add(new_account)
    session.commit()
    session.refresh(new_account)
    return new_account


@router.get("", response_model=list[AccountOut])
def list_accounts(session: Annotated[Session, Depends(get_db)]):
    return session.scalars(select(Account).order_by(Account.name.asc())).all()
