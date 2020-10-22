from fastapi import FastAPI
from loginfunctions import *


app = FastAPI()

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

