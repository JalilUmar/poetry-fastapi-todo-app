from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from user.utils import verify_access_token
from database import engine
from sqlmodel import Session

from typing import Annotated


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


def get_db():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authentication": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)
