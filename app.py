from fastapi import FastAPI
from loginfunctions import *


app = FastAPI()

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.email_address, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    if current_user.verified == 0:
        raise HTTPException(status_code=400, detail="Email no verified")
    return current_user.email_address
