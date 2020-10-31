from pydantic import BaseModel, EmailStr


class UserTemp(BaseModel):
    username: str
    email: str
    password: str

class ConfigGame(BaseModel):
    name: str
    max_players: int
    email: str
