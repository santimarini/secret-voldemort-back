from fastapi import FastAPI
## from fastapi_users.authentication import JWTAuthentication
from loginfunctions import *
## from pony import

app = FastAPI()

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    print(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.email, "token_type": "bearer"}

## get_current_verified_user podemos verificar si tiene el email verificado
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_verified_user)):
    return current_user

#@app.post("/user/validateemail")
#async def validate_email(recibo un token conA)
#    deberia modificar la base de datos