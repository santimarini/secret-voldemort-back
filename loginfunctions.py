from users import *
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_hash_password(password: str):
    return "fakehashed" + password

def get_user(db, email: EmailStr):
    if email in db:
        user_dict = db[email]
        return UserInDB(**user_dict)

## decode toke
def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: EmailStr = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials bla",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_user(token: EmailStr = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials asd",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_verified_user(current_user: User = Depends(get_current_user)):
    if current_user.verified:
        raise HTTPException(status_code=400, detail="Email no verified")
    return current_user