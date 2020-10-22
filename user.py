from pydantic import BaseModel, EmailStr


class UserTemp(BaseModel):
    name: str
    email_address: EmailStr
    password: str

