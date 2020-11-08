from pydantic import BaseModel, EmailStr
from typing import List


class UserTemp(BaseModel):
    alias: str
    email: str
    password: str

class ConfigGame(BaseModel):
    name: str
    max_players: int

class EmailSchema(BaseModel):
    email: List[EmailStr]