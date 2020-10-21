from fastapi import FastAPI, HTTPException, status
from database.database import *
from user import *

app = FastAPI(
    title="Secret Voldemort",
    description="Ingenieria del Software 2020 - Desaproba2",
    version="0.1"
)


# Register user
@app.post(
    "/user/",
    response_model=UserTemp,
    status_code=status.HTTP_201_CREATED
)
async def register_user(userNew: UserTemp):
    if check_data_consistency(userNew):
        # To do:
        # Verifies the existence of the user
        # if so, create user; if not, error
        # password hashing

        return new_user(userNew.name, userNew.email_address,
            userNew.password, "photo")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="incorrect user data"
        )