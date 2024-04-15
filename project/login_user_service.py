from datetime import datetime, timedelta
from typing import Optional

import prisma
import prisma.models
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class UserInfo(BaseModel):
    """
    A subset of the User model containing non-sensitive information to be shared upon successful login.
    """

    id: str
    email: str
    role: str


class UserLoginResponse(BaseModel):
    """
    Response object for successful authentication, including the JWT token and user information.
    """

    access_token: str
    token_type: str
    user: UserInfo


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


SECRET_KEY = "secret_jwt_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(email: str, password: str) -> Optional[prisma.models.User]:
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user:
        return None
    if not pwd_context.verify(password, user.hashedPassword):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login_user(email: str, password: str) -> UserLoginResponse:
    """
    Endpoint for user login, providing authentication tokens

    Args:
      email (str): The user's email address used for registration.
      password (str): The user's password.

    Returns:
      UserLoginResponse: Response object for successful authentication, including the JWT token and user information.
    """
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return UserLoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserInfo(id=user.id, email=user.email, role=user.role),
    )
