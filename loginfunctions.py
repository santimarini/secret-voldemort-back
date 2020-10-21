from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_hash_password(password: str):
    return "fakehashed" + password

## decode toke
def fake_decode_token(token):
    user = get_user_by_email(token)
    if user is not None:
        return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials bla",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

