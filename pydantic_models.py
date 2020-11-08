from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserTemp(BaseModel):
    alias: str
    email: str
    password: str


class ConfigGame(BaseModel):
    name: str
    max_players: int


class EmailSchema(BaseModel):
    email: List[EmailStr]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
