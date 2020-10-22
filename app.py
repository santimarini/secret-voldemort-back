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

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # return token to identify a specific user, it'll be the user's email for simplicity
    return {"access_token": user.email_address, "token_type": "bearer"}
