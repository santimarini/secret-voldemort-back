from fastapi import Depends, HTTPException, status, BackgroundTasks, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.database import *
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional
from pydantic_models import *
from datetime import date, datetime, timedelta
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
import re

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080
VALIDATE_TOKEN_EXPIRE_MINUTES = 120


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

conf = ConnectionConfig(
    MAIL_USERNAME = "secretvoldemort.game@gmail.com",
    MAIL_PASSWORD = "desaproba2/k60",
    MAIL_FROM = "secretvoldemort.game@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False
)


def get_message(email: EmailSchema, html):
    message = MessageSchema(
        subject="Email verification - no reply",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass
        body=html,
        subtype="html"
        )

    return message

def generate_html(user: str,validate_token:str):
    html = """
    <html>
    <body>
    <p>Hi! """ + user + """ Thanks for register in secret-voldemort.com
    <br>Please follow the next link to verified account and play!
    <br>http://localhost:3000/validate/""" + validate_token +"""</p>
    </body>
    </html>
    """
    return html

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_verified_user(current_user: User = Depends(get_current_user)):
    if not current_user.verified:
        raise HTTPException(status_code=400, detail="Email no validated")
    return current_user
    