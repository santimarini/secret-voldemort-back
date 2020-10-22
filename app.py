from fastapi import FastAPI, status, HTTPException
from database.database import *
from user import *
from loginfunctions import *


app = FastAPI(
    title="Secret Voldemort",
    description="Ingenieria del Software 2020 - Desaproba2",
    version="0.1"
)


# Register user
@app.post(
    "/user/",
    response_model=str,
    status_code=status.HTTP_200_OK
)
async def register_user(user_to_reg: UserTemp):

    if email_exists(user_to_reg.email_address):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="existing user"
        )
    else:
        new_user(user_to_reg.name, user_to_reg.email_address,
                 hash_password(user_to_reg.password), "photo")
