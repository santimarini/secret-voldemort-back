from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr
    verified: bool = False

class UserInDB(User):
    hashed_password: str

class UserOut(BaseModel):
    id: int
    name: str
    operation_result: str

fake_users_db = {
    "johndoe@example.com": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "verified": False,
    },
    "alice@example.com": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "verified": True,
    },
}