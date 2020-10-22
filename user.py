from pydantic import BaseModel, EmailStr


class UserTemp(BaseModel):
    username: str
    email: str
    password: str

