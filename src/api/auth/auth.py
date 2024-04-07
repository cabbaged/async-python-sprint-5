from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas import user_schema
from schemas.user_schema import UserCreate
from services.password_manager import PasswordManager
from services.user import user_crud

router = APIRouter()


@router.post("/register/", response_model=user_schema.UserResponse)
async def register(user: user_schema.User, db: AsyncSession = Depends(get_session),
             password_manager = Depends(PasswordManager.create)):
    db_user = await user_crud.get(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await user_crud.create(
        db, obj_in=UserCreate(username=user.username, hashed_password=password_manager.hash_password(user.password))
    )


@router.post("/auth/")
async def authenticate(user: user_schema.User, db: AsyncSession = Depends(get_session),
                 password_manager = Depends(PasswordManager.create)):
    db_user = await user_crud.get(db, username=user.username)
    if not db_user or not password_manager.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = password_manager.create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
