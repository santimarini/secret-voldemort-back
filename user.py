from pydantic import BaseModel, EmailStr


class UserTemp(BaseModel):
    name: str
    email_address: EmailStr
    password: str


def check_data_consistency(user_to_check: UserTemp) -> bool:
    if user_to_check.name.isalnum() and user_to_check.password.isalnum():
        return True
    else:
        return False
