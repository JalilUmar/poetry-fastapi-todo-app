from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select

from typing import Annotated
from dependencies import get_db, get_current_user
from .models import UserModel
from .schema import RegisterUserSchema, LoginResponse
from nanoid import generate
from .utils import get_password_hash, create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/api/users")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    request: RegisterUserSchema, db: Annotated[Session, Depends(get_db)]
):
    hash = get_password_hash(request.password)

    new_user = UserModel(
        id=str(generate()),
        username=request.username,
        email=request.email,
        password=hash,
    )

    db.add(new_user)
    db.commit()
    # db.refresh(new_user)

    return {
        "success": True,
        "message": "User registered successfully",
    }


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login_user(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    # user = db.query(UserModel).filter(UserModel.username == request.username).first()
    user = db.exec(
        select(UserModel).where(UserModel.username == request.username)
    ).first()

    verify = verify_password(request.password, user.password)

    if not user or not verify:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password!"
        )

    access_token = create_access_token(data={"sub": user.id})

    return {
        "success": True,
        "message": "User logged in successfully",
        "access_token": access_token,
        "token_type": "bearer",
    }
